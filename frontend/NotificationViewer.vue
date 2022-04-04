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
  <li
      id="notification-viewer"
      class="dropdown"
  >
    <a
        class="dropdown-toggle"
        data-toggle="dropdown"
        role="button"
        aria-haspopup="true"
        aria-expanded="false"
        @click="animationEnabled = false"
    >
      <div
          class="bell"
          :data-count="unreadNotificationsCount"
          :class="{'show-count': unreadNotificationsCount, 'notify': (unreadNotificationsCount && animationEnabled)}"
      >
        <span class="fas fa-bell" />
      </div>
    </a>
    <ul
        class="dropdown-menu notification-dropdown"
    >
      <li v-if="!loading && notifications.length">
        <a
            class="btn"
            :class="{ disabled: !unreadNotificationsCount }"
            @click="markAllAsRead"
        >
          {{ $t('notification_viewer.mark_all_as_read') }}
        </a>
      </li>
      <li
          v-if="error"
          role="separator"
          class="divider"
      />
      <li v-if="error">
        <div
            class="alert alert-warning"
            role="alert"
        >
          {{ error }}
        </div>
      </li>
      <li
          v-if="!loading && notifications.length"
          role="separator"
          class="divider"
      />
      <li
          v-if="!loading && !notifications.length"
      >
        {{ $t('notification_viewer.no_notifications') }}
      </li>
      <Notification
          v-for="notification in notifications"
          :key="notification.uuid"
          :uuid="notification.uuid"
          :state="notification.state"
          :sent-at="notification.sent_at"
          :payload="notification.payload"
          :truncate-length="truncateLength"
          @toggle="toggleState"
      />
      <li
          v-if="loading"
          class="progress"
      >
        <div
            class="progress-bar progress-bar-striped active"
            role="progressbar"
            aria-valuenow="100"
            aria-valuemin="0"
            aria-valuemax="100"
            style="width: 100%"
        >
          <span class="sr-only">
            {{ $t('notification_viewer.loading') }}
          </span>
        </div>
      </li>
      <li
          v-else-if="hasNextPage"
          class="text-center"
      >
        <button
            type="button"
            class="btn btn-link"
            @click="loadMore"
        >
          {{ $t('notification_viewer.load_more') }}
        </button>
      </li>
    </ul>
  </li>
</template>

<script>
import Notification from './components/Notification';
import { getCookie } from './utils';

export default {
  name: 'NotificationViewer',
  components: { Notification },
  props: {
    baseUrl: {
      type: String,
      required: true,
    },
    interval: {
      type: Number,
      default: 300,
    },
    limit: {
      type: Number,
      default: 15,
    },
    truncateLength: {
      type: Number,
      default: 60,
    },
  },
  data() {
    return {
      notifications: [],
      hasNextPage: false,
      animationEnabled: false,
      pageSize: this.limit,
      error: '',
      loading: true,
      unreadNotificationsCount: 0,
    };
  },
  async mounted() {
    await this.fetchNotifications();
    this.timer = setInterval(this.fetchNotifications, this.interval * 1000);
    // This next line let the dropdown menu open after clicking inside it. See the bootstrap source code here:
    // https://github.com/twbs/bootstrap/blob/0b9c4a4007c44201dce9a6cc1a38407005c26c86/js/dropdown.js#L160
    jQuery(document).on('click.bs.dropdown.data-api', '.notification-dropdown', e => e.stopPropagation());
  },
  methods: {
    fetchNotifications: async function () {
      try {
        const response = await fetch(`${this.baseUrl}?limit=${this.pageSize}`);
        const newNotifications = await response.json();
        if (newNotifications.count) {
          this.animationEnabled = true;
        }
        this.notifications = newNotifications.results;
        this.hasNextPage = !!newNotifications.next;
        this.unreadNotificationsCount = newNotifications.unread_count;
      } catch (error) {
        this.error = `${this.$t('notification_viewer.error_fetch_notifications')} ( ${error.statusText} )`;
      } finally {
        this.loading = false;
      }
    },
    toggleState: async function (uuid) {
      try {
        const response = await fetch(`${this.baseUrl}${uuid}`, {
          method: 'PATCH',
          headers: {'X-CSRFToken': getCookie('csrftoken')},
        });
        if (response.status === 200) {
          const notificationIndex = this.notifications.findIndex((notification) => notification.uuid === uuid);
          const newNotification = await response.json();
          this.$set(this.notifications, notificationIndex, newNotification);
          // update unread notifications count
          if (newNotification.state === 'SENT_STATE') {
            this.unreadNotificationsCount++;
          } else {
            this.unreadNotificationsCount--;
          }
          // if all the notifications are read and there is still unread notification, fetch all the notifications
          // to display the ones that are not read first.
          if (this.notifications.filter(n => n.state === 'SENT_STATE').length !== this.unreadNotificationsCount) {
            await this.fetchNotifications();
          }
        } else {
          this.error = `${this.$t('notification_viewer.error_mark_as_read')}`;
        }
      } catch (error) {
        this.error = `${this.$t('notification_viewer.error_mark_as_read')} ( ${error.statusText} )`;
      }
    },
    markAllAsRead: async function () {
      try {
        const response = await fetch(`${this.baseUrl}mark_all_as_read`, {
          method: 'PUT',
          headers: {'X-CSRFToken': getCookie('csrftoken')},
        });
        const notifications = await response.json();
        if (response.status === 200 && notifications.length > 0) {
          this.notifications.forEach(notification => notification.state = "READ_STATE");
          this.unreadNotificationsCount = 0;
        } else {
          this.error = `${this.$t('notification_viewer.error_mark_all_as_read')}`;
        }
      } catch (error) {
        this.error = `${this.$t('notification_viewer.error_mark_all_as_read')} ( ${error.statusText} )`;
      }
    },
    /**
     * We use the ?limit to get new tasks when clicking on the 'Load more' button as we need to keep all the previous
     * tasks and add the new ones. All this will be override by the setInterval that fetch all the async tasks if we
     * use the ?offset. So it may generate a big request, but it is very unlikely.
     */
    loadMore: function (e) {
       e.stopPropagation();
      this.loading = true;
      this.pageSize += this.limit;
      this.fetchNotifications();
    },
  },
};
</script>

<style lang="scss">
#notification-viewer {
  .alert.alert-warning {
    margin-top: 20px;
  }

  .notification-dropdown {
    min-width: 70vw;
    padding: 15px;
    overflow-y: scroll;
    max-height: 320px;
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
  &::after {  // notification count
    font-family: Arial sans-serif;
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
    transform: scale(0.5);
    transition: transform, opacity;
    transition-duration: 0.3s;
    transition-timing-function: ease-out;
    color: #fff;
    z-index: 2;
  }
  &.notify span {
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
