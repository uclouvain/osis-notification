<!--
  -
  - OSIS stands for Open Student Information System. It's an application
  - designed to manage the core business of higher education institutions,
  - such as universities, faculties, institutes and professional schools.
  - The core business involves the administration of students, teachers,
  - courses, programs and so on.
  -
  - Copyright (C) 2015-2023 Université catholique de Louvain (http://www.uclouvain.be)
  -
  - This program is free software: you can redistribute it and/or modify
  - it under the terms of the GNU General Public License as published by
  - the Free Software Foundation, either version 3 of the License, or
  - (at your option) any later version.
  -
  - This program is distributed in the hope that it will be useful,
  - but WITHOUT ANY WARRANTY; without even the implied warranty of
  - MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  - GNU General Public License for more details.
  -
  - A copy of this license - GNU General Public License - is available
  - at the root of the source code of this program.  If not,
  - see http://www.gnu.org/licenses/.
  -
  -->

<template>
  <div :class="containerCssClass">
    <div
        :class="[isTruncated ? 'truncated' : '', contentCssClass]"
        v-html="isTruncated ? truncatedHtml : htmlText"
    />
    <button
        v-if="truncatedHtml.length < htmlText.length"
        :class="buttonCssClass"
        @click.prevent="isTruncated = !isTruncated"
    >
      {{ isTruncated ? moreButtonText : lessButtonText }}
    </button>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import truncate from 'html-truncate';

export default defineComponent({
  name: 'TruncateHtml',
  props: {
    htmlText: {
      type: String,
      default: '',
    },
    length: {
      type: Number,
      default: 100,
    },
    lessButtonText: {
      type: String,
      default: "Show less",
    },
    contentCssClass: {
      type: String,
      default: "",
    },
    containerCssClass: {
      type: String,
      default: "",
    },
    buttonCssClass: {
      type: String,
      default: "",
    },
    moreButtonText: {
      type: String,
      default: "Show more",
    },
  },
  data() {
    return {
      isTruncated: true,
      truncatedHtml: truncate(this.htmlText, this.length),
    };
  },
});
</script>
