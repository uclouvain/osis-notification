/*
 *
 *   OSIS stands for Open Student Information System. It's an application
 *   designed to manage the core business of higher education institutions,
 *   such as universities, faculties, institutes and professional schools.
 *   The core business involves the administration of students, teachers,
 *   courses, programs and so on.
 *
 *   Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   A copy of this license - GNU General Public License - is available
 *   at the root of the source code of this program.  If not,
 *   see http://www.gnu.org/licenses/.
 *
 */

import { mount } from '@vue/test-utils';
import Notification from './Notification.vue';

jest.mock('../utils.js');


const notificationSentData = {
  uuid: '5646548946464',
  state: 'SENT_STATE',
  sentAt: Date.now().toString(),
  payload: 'This is a test payload with a SENT_STATE',
}
const notificationReadData = {
  uuid: '5646548946464',
  state: 'READ_STATE',
  sentAt: Date.now().toString(),
  readAt: Date.now().toString(),
  payload: 'This is a test payload with a READ_STATE',
}

describe('component lifecycle', () => {
  const tooltip = jest.fn();
  window.jQuery = jest.fn(() => ({
    tooltip,
  }));

  it('should mount', () => {
    const wrapper = mount(Notification, {
      propsData: {
        ...notificationSentData,
      },
      mocks: {
        jQuery,
        $t: k => k,
      },
    });
    expect(wrapper.text()).toContain(notificationSentData['payload']);
    expect(wrapper.text()).toContain(notificationSentData['sentAt']);
    expect(window.jQuery).toHaveBeenCalled();
  });

  it('should update', async () => {
    const wrapper = mount(Notification, {
      propsData: {
        ...notificationSentData,
      },
      mocks: {
        jQuery,
        $t: k => k,
      },
    });
    tooltip.mockClear();
    expect(tooltip).not.toHaveBeenCalled();
    // change this and trigger an update
    wrapper.setProps({...notificationReadData});
    await wrapper.vm.$nextTick();
    expect(tooltip).toHaveBeenCalled();
  });

});

it('should trigger toggle', async () => {
  const wrapper = mount(Notification, {
    propsData: {
      ...notificationSentData,
    },
    mocks: {
      jQuery,
      $t: k => k,
    },
  });
  expect(wrapper.emitted('toggle')).toBeFalsy();
  await wrapper.find('input').trigger('click');
  expect(wrapper.emitted('toggle')).toBeTruthy();
});

it('should have correct computed values', () => {
  expect(Notification.computed.isSent.call({ state: notificationSentData.state})).toEqual(true);
  expect(Notification.computed.isSent.call({ state: notificationReadData.state})).toEqual(false);
});

describe('radio button', () => {
  it('should be ticked if notification state is `SENT_STATE`', () => {
      const wrapper = mount(Notification, {
      propsData: {
        ...notificationSentData,
      },
      mocks: {
        jQuery,
        $t: k => k,
      },
    });
    const input = wrapper.find('input[type="radio"]');
    expect(input.element.checked).toEqual(true);
  });

  it('should not be ticked if notification state is `READ_STATE`', () => {
      const wrapper = mount(Notification, {
      propsData: {
        ...notificationReadData,
      },
      mocks: {
        jQuery,
        $t: k => k,
      },
    });
    const input = wrapper.find('input[type="radio"]');
    expect(input.element.checked).toEqual(false);
  });
});
