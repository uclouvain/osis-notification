<!--
  -
  -   OSIS stands for Open Student Information System. It's an application
  -   designed to manage the core business of higher education institutions,
  -   such as universities, faculties, institutes and professional schools.
  -   The core business involves the administration of students, teachers,
  -   courses, programs and so on.
  -
  -   Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
  -
  -   This program is free software: you can redistribute it and/or modify
  -   it under the terms of the GNU General Public License as published by
  -   the Free Software Foundation, either version 3 of the License, or
  -   (at your option) any later version.
  -
  -   This program is distributed in the hope that it will be useful,
  -   but WITHOUT ANY WARRANTY; without even the implied warranty of
  -   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  -   GNU General Public License for more details.
  -
  -   A copy of this license - GNU General Public License - is available
  -   at the root of the source code of this program.  If not,
  -   see http://www.gnu.org/licenses/.
  -
  -->
<template>
  <li class="dropdown notification-viewer">
    <a
        class="dropdown-toggle"
        data-toggle="dropdown"
        role="button"
        aria-haspopup="true"
        aria-expanded="false"
    >
      <div
          class="bell"
          :data-count="unreadNotificationsCount"
          :class="{'show-count': unreadNotificationsCount, 'notify': unreadNotificationsCount}"
      />
    </a>
    <ul
        v-show="notifications.length"
        class="dropdown-menu notification-dropdown"
    >
      <li>
        <a
            class="btn"
            :class="{ disabled: !unreadNotificationsCount }"
            @click="markAllAsRead"
        >
          {{ $t('mark_all_as_read') }}
        </a>
      </li>
      <li
          role="separator"
          class="divider"
      />
      <li
          v-for="notification in notifications"
          :key="notification.uuid"
          class="notification-dropdown-item"
          v-bind="notification"
      >
        <a>
          <div class="radio">
            <input
                :id="notification.uuid"
                v-model="notification.state"
                :value="'SENT_STATE'"
                type="radio"
                data-toggle="tooltip"
                data-placement="top"
                :title="notification.state === 'SENT_STATE' ? $t('mark_as_read') : $t('mark_as_unread')"
                @click="markAsRead(notification)"
            >
            <span class="label label-primary">{{ notification.sent_at }}</span>
            <!-- Disable the vue/no-v-html warning -->
            <!-- eslint-disable-next-line -->
            <span class="notification-text" :class="{ 'font-bold': notification.state === 'SENT_STATE' }" v-html="notification.payload" />
          </div>
        </a>
      </li>
    </ul>
    <div
        v-if="error"
        class="alert alert-warning"
        role="alert"
    >
      {{ error }}
    </div>
  </li>
</template>

<script>

export default {
  name: 'NotificationViewer',
  props: {
    url: {
      type: String,
      default: '',
    },
    interval: {
      type: Number,
      default: 300,
    },
  },
  data() {
    return {
      notifications: [],
      error: '',
    };
  },
  computed: {
    unreadNotificationsCount: function () {
      return this.notifications.filter(notification => notification.state === 'SENT_STATE').length;
    },
  },
  async mounted() {
    await this.fetchNotifications();
    this.timer = setInterval(this.fetchNotifications, this.interval * 1000);
    // This next line let the dropdown menu open after clicking inside it. See the bootstrap source code here:
    // https://github.com/twbs/bootstrap/blob/0b9c4a4007c44201dce9a6cc1a38407005c26c86/js/dropdown.js#L160
    jQuery(document).on('click.bs.dropdown.data-api', '.notification-dropdown', e => e.stopPropagation());
    // activate the tooltips
    jQuery(() => jQuery('[data-toggle="tooltip"]').tooltip());
  },
  methods: {
    fetchNotifications: async function () {
      try {
        if (this.url) {
          const response = await fetch(this.url);
          let newNotifications = await response.json();
          this.notifications = newNotifications.results;
        }
      } catch (error) {
        this.error = this.$t('error_fetch_notifications').concat(' (', error.statusText, ')');
      }
    },
    markAsRead: async function (notification) {
      try {
        const response = await fetch(this.url.concat(notification.uuid), {
          method: 'PATCH',
          headers: {'X-CSRFToken': this.getCookie('csrftoken')},
        });
        if (response.status === 200) {
          const notificationIndex = this.notifications.indexOf(notification);
          let newNotification = await response.json();
          this.$set(this.notifications, notificationIndex, newNotification);
          // Change the bootstrap input radio tooltip
          jQuery('#'.concat(notification.uuid))
              .attr('data-original-title', newNotification.state === 'SENT_STATE' ? this.$t('mark_as_read') : this.$t('mark_as_unread'))
              .tooltip('show');
        }
      } catch (error) {
        this.error = this.$t('error_mark_as_read').concat(' (', error.statusText, ')');
      }
    },
    markAllAsRead: async function () {
      try {
        const response = await fetch(this.url.concat('mark_all_as_read'), {
          method: 'PUT',
          headers: {'X-CSRFToken': this.getCookie('csrftoken')},
        });
        let notifications = await response.json();
        if (response.status === 200 && notifications.length > 0) {
          this.notifications = notifications;
          // Change ALL the bootstrap input radio tooltips
          jQuery('[data-toggle="tooltip"]').attr('data-original-title', this.$t('mark_as_unread'));
        }
      } catch (error) {
        this.error = this.$t('error_mark_all_as_read').concat(' (', error.statusText, ')');
      }
    },
    /**
     * Get the given cookie from it's name. We use it to get the csrftoken.
     * See code from https://docs.djangoproject.com/en/3.2/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
     */
    // TODO check les conditions de getCookie
    getCookie: function (name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
  },
};
</script>

<style lang="scss">
.notification-viewer {
  .alert.alert-warning {
    margin-top: 20px;
  }

  .notification-dropdown {
    width: 70vh;
    padding: 15px;

    .notification-dropdown-item {
      .label {
        margin-left: 30px;
      }

      input[type=radio] {
        cursor: pointer;
        margin-left: -5px;
      }

      .notification-text {
        display: block;
        text-align: justify;
        white-space: initial;
        margin-top: 10px;
        margin-left: 30px;
      }
    }

    .font-bold {
      font-weight: bold;
    }
  }
}

//-------------------------------------------------
// Code from https://codepen.io/ryanmorr/pen/RPZZjd
.bell {
  display: inline-block;
  position: relative;

  &::before,
  &::after {
    color: #777;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }
  &::before {
    display: block;
    content: "\f0f3";
    font-family: "Font Awesome 5 Free";
    transform-origin: top center;
  }
  &::after {
    font-family: Arial;
    font-size: 0.8em;
    font-weight: 700;
    position: absolute;
    top: -10px;
    right: -15px;
    padding: 1px 3px;
    line-height: 100%;
    border: 2px #fff solid;
    border-radius: 60px;
    background: #db3434;
    opacity: 0;
    content: attr(data-count);
    opacity: 0;
    transform: scale(0.5);
    transition: transform, opacity;
    transition-duration: 0.3s;
    transition-timing-function: ease-out;
    color: #fff;
    z-index: 2;
  }
  &.notify::before {
    animation: ring 1.5s ease;
    animation-iteration-count: infinite;
  }
  &.show-count::after {
    transform: scale(1);
    opacity: 1;
  }
  @keyframes ring {
    0% { transform: rotate(35deg); }
    12.5% { transform: rotate(-30deg); }
    25% { transform: rotate(25deg); }
    37.5% { transform: rotate(-20deg); }
    50% { transform: rotate(15deg); }
    62.5% { transform: rotate(-10deg); }
    75% { transform: rotate(5deg); }
    100% { transform: rotate(0deg); }
  }
}
//-------------------------------------------------
</style>
