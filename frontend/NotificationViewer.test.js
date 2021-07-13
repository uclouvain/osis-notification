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
import NotificationViewer from './NotificationViewer.vue';
import fetchMock from "fetch-mock";
import Vue from "vue";

jest.mock('./utils.js');

const mockSentNotifications = {
  count: 1,
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
fetchMock.get('/?limit=15', mockSentNotifications)
  .get('/error', {throws: 'This is an error'})
  .put('/mark_all_as_read', function () {
    mockSentNotifications.results.forEach(notification => {
      notification.state = 'READ_STATE';
      notification.read_at = Date.now();
    });
    return mockSentNotifications.results;
  })
  .patch('*', function () {
    let notification = mockSentNotifications.results[0]
    notification.state = (notification.state === "READ_STATE") ? "SENT_STATE" : "READ_STATE";
    notification.read_at = (notification.state === "READ_STATE") ? Date.now() : null;
    return notification;
  });

describe('component lifecycle', () => {
  const on = jest.fn();
  window.jQuery = jest.fn(() => ({
    on,
  }));

  it('should mount', async () => {
    const wrapper = mount(NotificationViewer, {
      propsData: {
        url: '/',
      },
      mocks: {
        jQuery,
        $t: k => k,
      },
    });

    expect(wrapper.text()).toContain('notification_viewer.mark_all_as_read');
    expect(on).toHaveBeenCalled();
    expect(wrapper.vm.notifications.length).toBe(0);
    await Vue.nextTick(); // wait for request
    await Vue.nextTick(); // wait for loading
    await Vue.nextTick(); // wait for re-rendering
    expect(wrapper.vm.notifications.length).toBe(1);
  });

  it('should display an error if fetching notifications fail', async () => {
    const wrapper = mount(NotificationViewer, {
      propsData: {
        url: '/error',
      },
      mocks: {
        jQuery,
        $t: k => k,
      },
    });
    await Vue.nextTick(); // wait for loading
    await Vue.nextTick(); // wait for re-rendering
    expect(wrapper.text()).toContain('notification_viewer.error_fetch_notifications');
    expect(on).toHaveBeenCalled();
    expect(wrapper.vm.notifications.length).toBe(0);
  });
});

describe('toggle notification state', () => {
  const wrapper = mount(NotificationViewer, {
    propsData: {
      url: '/',
    },
    mocks: {
      jQuery,
      $t: k => k,
    },
  });
  it('should update the notifications array', async () => {
    expect(wrapper.vm.notifications[0].state).toBe('SENT_STATE');
    await wrapper.vm.toggleState(mockSentNotifications.results[0].uuid);
    expect(wrapper.vm.notifications[0].state).toBe('READ_STATE');
  });
  it('should update the notifications array once again', async () => {
    expect(wrapper.vm.notifications[0].state).toBe('READ_STATE');
    await wrapper.vm.toggleState(mockSentNotifications.results[0].uuid);
    expect(wrapper.vm.notifications[0].state).toBe('SENT_STATE');
  });
  it('should display an error if fetching notifications fail', async () => {
    fetchMock.patch('*', {throws: 'This is an error'}, {overwriteRoutes: true});
    await wrapper.vm.toggleState(mockSentNotifications.results[0].uuid);
    await Vue.nextTick(); // wait for loading
    await Vue.nextTick(); // wait for re-rendering
    expect(wrapper.text()).toContain('notification_viewer.error_mark_as_read');
  });
  it('should display an error if fetching notifications does not return 200', async () => {
    fetchMock.patch('*', {status: 404}, {overwriteRoutes: true});
    await wrapper.vm.toggleState(mockSentNotifications.results[0].uuid);
    await Vue.nextTick(); // wait for loading
    await Vue.nextTick(); // wait for re-rendering
    expect(wrapper.text()).toContain('notification_viewer.error_mark_as_read');
  });
});

describe('mark all notifications as read', () => {
  const wrapper = mount(NotificationViewer, {
    propsData: {
      url: '/',
    },
    mocks: {
      jQuery,
      $t: k => k,
    },
  });
  it('should change the notification state to read', async () => {
    expect(wrapper.vm.notifications[0].state).toBe('SENT_STATE');
    await wrapper.vm.markAllAsRead();
    expect(wrapper.vm.notifications[0].state).toBe('READ_STATE');
    expect(wrapper.vm.notifications[0].read_at).not.toBe(null);
  });
  it('should display an error if marking notifications as read fail', async () => {
    fetchMock.put('/mark_all_as_read', {throws: 'This is an error'}, {overwriteRoutes: true});
    await wrapper.vm.markAllAsRead();
    await Vue.nextTick(); // wait for loading
    await Vue.nextTick(); // wait for re-rendering
    expect(wrapper.text()).toContain('notification_viewer.error_mark_all_as_read');
  });
  it('should display an error if fetching notifications does not return 200', async () => {
    fetchMock.put('/mark_all_as_read', {data: null, status: 404}, {overwriteRoutes: true});
    await wrapper.vm.markAllAsRead();
    await Vue.nextTick(); // wait for loading
    await Vue.nextTick(); // wait for re-rendering
    expect(wrapper.text()).toContain('notification_viewer.error_mark_all_as_read');
  });
});
