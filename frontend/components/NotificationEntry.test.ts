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

import {mount} from '@vue/test-utils';
import NotificationEntry from './NotificationEntry.vue';
import {describe, expect, it, vi} from "vitest";


const tooltip = vi.fn((eventName, selectorOrHandler: string | CallableFunction, handler?: CallableFunction) => {
  if (typeof selectorOrHandler === 'function') {
    selectorOrHandler({stopPropagation: vi.fn()});
  } else if (handler) {
    handler({stopPropagation: vi.fn()});
  }
});
const jQueryMock = vi.fn(() => ({
  tooltip: tooltip,
}));

vi.stubGlobal('jQuery', jQueryMock);

const notificationSentData = {
  uuid: '5646548946464',
  state: 'SENT_STATE',
  sentAt: Date.now().toString(),
  payload: 'This is a test payload with a SENT_STATE',
};
const notificationReadData = {
  uuid: '5646548946464',
  state: 'READ_STATE',
  sentAt: Date.now().toString(),
  readAt: Date.now().toString(),
  payload: 'This is a test payload with a READ_STATE',
};

describe('component lifecycle', () => {

  it('should mount', () => {
    const wrapper = mount(NotificationEntry, {props: {...notificationSentData}});
    expect(wrapper.text()).toContain(notificationSentData['payload']);
    expect(wrapper.text()).toContain(notificationSentData['sentAt']);
    expect(tooltip).toHaveBeenCalled();
    tooltip.mockReset();

    wrapper.unmount();
    expect(tooltip).toHaveBeenCalled();
  });

  it('should update', async () => {
    const wrapper = mount(NotificationEntry, {props: {...notificationSentData}});
    tooltip.mockClear();
    expect(tooltip).not.toHaveBeenCalled();
    // change this and trigger an update
    await wrapper.setProps({...notificationReadData});
    expect(tooltip).toHaveBeenCalled();
  });
});

it('should trigger toggle', async () => {
  const onToggle = vi.fn();
  const wrapper = mount(NotificationEntry, {
    props: {
      ...notificationSentData,
      onToggle: onToggle,
    },
  });
  expect(wrapper.emitted()).not.toHaveProperty('toggle');
  const input = wrapper.get('input');
  expect(input.element.id).toBe('notification-5646548946464');
  await input.trigger('click.prevent');
  expect(onToggle).toHaveBeenCalled();
});

describe('notification display', () => {
  it('changes when sent state', async () => {
    const wrapper = mount(NotificationEntry, {props: {...notificationSentData}});

    // input must be checked
    const input = wrapper.find('input');
    expect(input.exists()).toBe(true);
    expect(input.element.checked).toBeTruthy();
    // text must be bold
    const textDiv = wrapper.find('.notification-text > div');
    expect(textDiv.exists()).toBe(true);
    expect(textDiv.classes()).toContain('font-bold');
    // input tooltip should call for mark as read action
    await input.trigger("mouseover");
    expect(input.element.getAttribute('data-original-title')).toBe('notification.mark_as_read');
  });

  it('changes when read state', async () => {
    const wrapper = mount(NotificationEntry, {props: {...notificationReadData}});

    // input must not be checked
    const input = wrapper.find('input');
    expect(input.exists()).toBe(true);
    expect(input.element.checked).toBeFalsy();
    // text must not be bold
    const textDiv = wrapper.find('.notification-text > div');
    expect(textDiv.exists()).toBe(true);
    expect(textDiv.classes()).not.toContain('font-bold');
    // input tooltip should call for mark as unread action
    await input.trigger("mouseover");
    expect(input.element.getAttribute('data-original-title')).toBe('notification.mark_as_unread');
  });
});

describe('radio button', () => {
  it('should be ticked if notification state is `SENT_STATE`', () => {
    const wrapper = mount(NotificationEntry, {props: {...notificationSentData}});
    const input = wrapper.find('input[type="radio"]');
    expect((input.element as HTMLInputElement).checked).toEqual(true);
  });

  it('should not be ticked if notification state is `READ_STATE`', () => {
    const wrapper = mount(NotificationEntry, {props: {...notificationReadData}});
    const input = wrapper.find('input[type="radio"]');
    expect((input.element as HTMLInputElement).checked).toEqual(false);
  });
});
