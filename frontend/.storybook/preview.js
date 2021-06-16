/*
 */

import { i18n } from "../i18n";
import { addDecorator } from '@storybook/vue';

// Internationalisation
addDecorator(() => ({
  i18n,
  beforeCreate: function() {
    this.$root._i18n = this.$i18n;
  },
  template: "<story/>"
}));
