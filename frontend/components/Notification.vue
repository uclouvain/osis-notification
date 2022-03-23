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
  <li class="notification-dropdown-item">
    <input
        :id="`notification-${uuid}`"
        :checked="isSent"
        type="radio"
        data-toggle="tooltip"
        data-placement="top"
        :data-original-title="isSent ? $t('notification.mark_as_read') : $t('notification.mark_as_unread')"
        @click.prevent="$emit('toggle', uuid)"
    >
    <span class="label label-primary">{{ sentAt }}</span>
    <truncate
        action-class="btn btn-link"
        class="notification-text"
        type="html"
        :class="{ 'font-bold': isSent }"
        :clamp="$t('notification.show_more')"
        :length="truncateLength"
        :less="$t('notification.show_less')"
        :text="payload"
    />
  </li>
</template>

<script>
import truncate from 'vue-truncate-collapsed';

export default {
  name: 'Notification',
  components: { truncate },
  props: {
    uuid: {
      type: String,
      required: true,
    },
    state: {
      type: String,
      required: true,
    },
    sentAt: {
      type: String,
      required: true,
    },
    payload: {
      type: String,
      required: true,
    },
    truncateLength: {
      type: Number,
      default: 60,
    },
  },
  computed: {
    isSent: function () {
      return this.state === 'SENT_STATE';
    },
  },
  mounted() {
    // activate the tooltips
    jQuery('[data-toggle="tooltip"]').tooltip();
  },
  updated() {
    // Show the bootstrap input radio tooltip
    jQuery(`#notification-${this.uuid}`).tooltip('show');
  },
};
</script>

<style lang="scss">
.notification-dropdown-item {
  &:hover {
    background-color: #f5f5f5;
  }

  .label {
    margin-left: 10px;
  }

  input[type=radio] {
    cursor: pointer;
    margin-left: 15px;
    margin-right: 15px;
  }

  .notification-text {
    display: block;
    white-space: initial;
    margin: 10px 10px 10px 55px;
  }
}

.font-bold {
  font-weight: bold;
}
</style>
