/*
 *
 * OSIS stands for Open Student Information System. It's an application
 * designed to manage the core business of higher education institutions,
 * such as universities, faculties, institutes and professional schools.
 * The core business involves the administration of students, teachers,
 * courses, programs and so on.
 *
 * Copyright (C) 2015-2023 Université catholique de Louvain (http://www.uclouvain.be)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * A copy of this license - GNU General Public License - is available
 * at the root of the source code of this program.  If not,
 * see http://www.gnu.org/licenses/.
 *
 */

import {mount} from '@vue/test-utils';
import TruncateHtml from './TruncateHtml.vue';
import {expect, it} from "vitest";


it('should not truncate if text is too short', () => {
  const wrapper = mount(TruncateHtml, {
    props: {
      htmlText: "<strong>Lorem ipsum dolor amet</strong>",
      length: 100,
    },
  });
  expect(wrapper.text()).toContain('Lorem ipsum dolor amet');
  expect(wrapper.find('button').exists()).toBeFalsy();
});


it('should truncate anthen show all', async () => {
  const wrapper = mount(TruncateHtml, {
    props: {
      htmlText: "<strong>Lorem ipsum dolor amet</strong>",
      length: 10,
    },
  });
  expect(wrapper.text()).toContain('Lorem');
  expect(wrapper.text()).not.toContain('dolor amet');
  await wrapper.find('button').trigger('click.prevent');
  expect(wrapper.text()).toContain('dolor amet');
});

