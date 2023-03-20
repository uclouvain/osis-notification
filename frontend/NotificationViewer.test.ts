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

import {flushPromises, mount} from '@vue/test-utils';
import NotificationViewer from './NotificationViewer.vue';
import fetchMock from "fetch-mock";
import {beforeEach, describe, expect, it, vi, test} from "vitest";
import type {EntriesResponse, EntryRecord} from "./interfaces";

function structuredClone<T>(obj: T): T {
  /** not available in node < 17 */
  return JSON.parse(JSON.stringify(obj)) as T;
}

const mockSentNotifications: EntriesResponse = {
  count: 1,
  unread_count: 1,
  previous: null,
  next: null,
  results: [
    {
      uuid: '1445bb87-4965-44a5-9889-1b82f49166ec',
      state: 'SENT_STATE',
      payload: 'This notification has already been read. And it have a super long text inside it, so you can see how the component will display something this long. Also, if you want to add more stories it is easy, please see the `NotificationViewer.stories.js` file.',
      created_at: '02/06/2021 12:22',
      sent_at: '02/06/2021 14:22',
      read_at: '02/06/2021 18:22',
    },
  ],
};

const on = vi.fn((eventName, selectorOrHandler: string | CallableFunction, handler?: CallableFunction) => {
  if (typeof selectorOrHandler === 'function') {
    selectorOrHandler({stopPropagation: vi.fn()});
  } else if (handler) {
    handler({stopPropagation: vi.fn()});
  }
});
const tooltip = vi.fn((eventName, selectorOrHandler: string | CallableFunction, handler?: CallableFunction) => {
  if (typeof selectorOrHandler === 'function') {
    selectorOrHandler({stopPropagation: vi.fn()});
  } else if (handler) {
    handler({stopPropagation: vi.fn()});
  }
});
const jQueryMock = vi.fn(() => ({
  on: on,
  tooltip: tooltip,
}));

vi.stubGlobal('jQuery', jQueryMock);

beforeEach(() => {
  window.document.cookie = 'csrftoken=1234-5678-9101-1121-3141';
});

test('should mount and unmount', async () => {
  fetchMock.restore().get('/?limit=15', mockSentNotifications);
  vi.useFakeTimers();

  const wrapper = mount(NotificationViewer, {props: {baseUrl: '/'}});
  expect(wrapper.text()).toContain('notification_viewer.loading');
  expect(on).toHaveBeenCalled();
  expect(wrapper.findAllComponents({name: 'NotificationEntry'})).toHaveLength(0);
  await flushPromises();
  expect(vi.getTimerCount()).toBe(1);
  expect(wrapper.findAllComponents({name: 'NotificationEntry'})).toHaveLength(1);
  expect(wrapper.text()).toContain('notification_viewer.mark_all_as_read');

  vi.advanceTimersToNextTimer();
  await flushPromises();

  wrapper.unmount();
  expect(vi.getTimerCount()).toBe(0);
});

test('should display an error if bd response', async () => {
  fetchMock.restore().get('/?limit=15', 500);
  const wrapper = mount(NotificationViewer, {props: {baseUrl: '/'}});
  await flushPromises();
  expect(wrapper.text()).toContain('notification_viewer.error');
  expect(on).toHaveBeenCalled();
  expect(wrapper.findAllComponents({name: 'NotificationEntry'})).toHaveLength(0);
});

test('should display an error if fetching notifications fail', async () => {
  fetchMock.restore().get('/?limit=15', {throws: new Error('This is an error')});
  const wrapper = mount(NotificationViewer, {props: {baseUrl: '/'}});
  await flushPromises();
  expect(wrapper.text()).toContain('notification_viewer.error');
  expect(on).toHaveBeenCalled();
  expect(wrapper.findAllComponents({name: 'NotificationEntry'})).toHaveLength(0);
});

test('should stop animation when clicked', async () => {
  fetchMock.restore().get('/?limit=15', mockSentNotifications);
  const wrapper = mount(NotificationViewer, {props: {baseUrl: '/'}});
  await flushPromises();
  const bell = wrapper.find('.bell');
  expect(bell.attributes("data-count")).toBe("1");
  expect(bell.classes()).toContain('show-count');
  expect(bell.classes()).toContain('notify');
  await wrapper.find('.dropdown-toggle').trigger('click');
  expect(bell.classes()).not.toContain('notify');
});


describe('interactions with api', () => {
  beforeEach(() => {
    const notifications = structuredClone(mockSentNotifications);
    notifications.results = [...notifications.results, ...notifications.results, ...notifications.results];
    fetchMock.restore()
        .get('/?limit=2', function () {
          const page = structuredClone(notifications);
          page.next = "/?limit=4";
          page.results = notifications.results.slice(0, 2);
          page.unread_count = notifications.results.filter(n => n.state !== "READ_STATE").length;
          return page;
        })
        .get('/?limit=4', function () {
          const page = structuredClone(notifications);
          page.next = null;
          page.unread_count = notifications.results.filter(n => n.state !== "READ_STATE").length;
          return page;
        })
        .put('/mark_all_as_read', function () {
          notifications.results.forEach(notification => {
            notification.state = 'READ_STATE';
            notification.read_at = Date.now().toString();
          });
          return notifications.results;
        })
        .patch('*', function (url) {
          const notification = notifications.results.find(n => url.includes(n.uuid)) as EntryRecord;
          notification.state = (notification.state === "READ_STATE") ? "SENT_STATE" : "READ_STATE";
          notification.read_at = (notification.state === "READ_STATE") ? Date.now().toString() : null;
          return notification;
        });
  });

  it('should update the notifications array', async () => {
    const wrapper = mount(NotificationViewer, {props: {baseUrl: '/', limit: 2}});
    await flushPromises();
    const input = wrapper.getComponent({name: 'NotificationEntry'}).get('input');
    expect(input.element.checked).toBe(true); // not read
    await input.trigger('click');
    await flushPromises();
    expect(wrapper.find('.bell').attributes("data-count")).toBe("0");
    expect(wrapper.getComponent({name: 'NotificationEntry'}).get('input').element.checked).toBe(false);

    await input.trigger('click');
    await flushPromises();
    expect(wrapper.find('.bell').attributes("data-count")).toBe("1");
    expect(wrapper.getComponent({name: 'NotificationEntry'}).get('input').element.checked).toBe(true);

    // error
    fetchMock.restore().patch('*', 500);
    await input.trigger('click');
    await flushPromises();
    expect(wrapper.text()).toContain('notification_viewer.error');
  });

  it('should update the read count when mark all as read clicked', async () => {
    const wrapper = mount(NotificationViewer, {props: {baseUrl: '/', limit: 2}});
    await flushPromises();
    expect(wrapper.find('.bell').attributes("data-count")).toBe("3");
    await wrapper.get(".dropdown-menu .btn").trigger('click');
    await flushPromises();
    expect(wrapper.find('.bell').attributes("data-count")).toBe("0");

    // error
    fetchMock.restore().put('*', 500);
    await wrapper.get(".dropdown-menu .btn").trigger('click');
    await flushPromises();
    expect(wrapper.text()).toContain('notification_viewer.error');
  });

  it('should load more', async () => {
    const wrapper = mount(NotificationViewer, {props: {baseUrl: '/', limit: 2}});
    await flushPromises();
    expect(wrapper.findAllComponents({name: 'NotificationEntry'})).toHaveLength(2);
    expect(wrapper.find('.text-center .btn-link').exists()).toBe(true);
    await wrapper.find('.text-center .btn-link').trigger('click');
    await flushPromises();
    expect(wrapper.findAllComponents({name: 'NotificationEntry'})).toHaveLength(3);
  });
});
