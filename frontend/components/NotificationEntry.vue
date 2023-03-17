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
        :data-original-title="isSent ? $t('notification.mark_as_read') : $t('notification.mark_as_unread')"
        @click.prevent="$emit('toggle', uuid)"
    >
    <span class="label label-primary">{{ sentAt }}</span>
    <TruncateHtml
        button-css-class="btn btn-link"
        container-css-class="notification-text"
        :content-css-class="isSent ? 'font-bold' : ''"
        :html-text="payload"
        :length="truncateLength"
        :less-button-text="$t('notification.show_less')"
        :more-button-text="$t('notification.show_more')"
    />
  </li>
</template>

<script lang="ts">
import TruncateHtml from './TruncateHtml.vue';
import {defineComponent} from "vue";
import type jQuery from "jquery";

declare global {
  interface Window {
    jQuery: typeof jQuery;
  }
}

export default defineComponent({
  name: 'NotificationEntry',
  components: {TruncateHtml},
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
  emits: ['toggle'],
  computed: {
    isSent: function () {
      return this.state === 'SENT_STATE';
    },
  },
  mounted() {
    // activate the tooltips
    window.jQuery('[data-toggle="tooltip"]').tooltip({
      trigger: 'hover',
      placement: 'top',
      container: 'body',
      template: '<div class="tooltip tooltip-notification" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
    });
  },
  updated() {
    // hide the bootstrap input radio tooltip on click
    window.jQuery(`#notification-${this.uuid}`).tooltip('hide');
  },
  beforeUnmount() {
    // hide the bootstrap input radio tooltip on click
    window.jQuery(`#notification-${this.uuid}`).tooltip('destroy');
  },
});
</script>

<style lang="scss">
.notification-dropdown-item {
  &:hover {
    background-color: #f5f5f5;
  }

  .label {
    margin-left: 1em;
    margin-right: 1em;
    margin-top: .2em;
    float: left;
  }

  input[type=radio] {
    cursor: pointer;
    float: left;
  }

  .notification-text {
    display: block;
    white-space: initial;
    margin: 1em 1em 1em 1.7em;
  }

  .notification-text > div.truncated {
    display: inline;
  }
}

.tooltip-notification .tooltip-inner {
  width: auto;
}

.font-bold {
  font-weight: bold;
}
</style>
