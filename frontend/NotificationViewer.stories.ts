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

import NotificationViewer from './NotificationViewer.vue';
import fetchMock from 'fetch-mock';
import type {Meta, StoryFn} from "@storybook/vue3";
import type {EntriesResponse, EntryRecord} from "./interfaces";

const mockNotifications : EntriesResponse = {
  count: 3,
  previous: null,
  unread_count: 2,
  next: 'mockNotifications2',
  results: [
    {
      uuid: '31d69bd7-07e3-4567-a8f3-1aab41d86061',
      state: 'SENT_STATE',
      payload: 'There is a plain text notification',
      created_at: '08/06/2021 16:23',
      sent_at: '08/06/2021 16:24',
      read_at: null,
    },
    {
      uuid: 'f66ecf3b-637c-413a-91a7-e318c27ce02f',
      state: 'SENT_STATE',
      payload: 'There is an <i>html</i> notification! and there is a link here : <a href="https://github.com/uclouvain/osis-notification" target="_blank">osis-notification on Github</a>',
      created_at: '07/06/2021 12:22',
      sent_at: '07/06/2021 14:22',
      read_at: null,
    },
    {
      uuid: '1445bb87-4965-44a5-9889-1b82f49166ec',
      state: 'READ_STATE',
      payload: 'This notification has already been read. And it have a super long text inside it, so you can see how the component will display something this long. Also, if you want to add more stories it is easy, please see the `NotificationViewer.stories.js` file.',
      created_at: '02/06/2021 12:22',
      sent_at: '02/06/2021 14:22',
      read_at: '02/06/2021 18:22',
    },
  ],
};

export const NoNotification: StoryFn<typeof NotificationViewer> = () => {
  fetchMock.restore().get('/?limit=15', {count: 0, results: []});
  return {
    components: {NotificationViewer},
    template: `
      <ul class="nav navbar-nav">
      <NotificationViewer baseUrl="/" />
      </ul>
    `,
  };
};

export const WithNotifications: StoryFn<typeof NotificationViewer> = () => {
  const notifications = structuredClone(mockNotifications);
  fetchMock.restore()
      .get('/?limit=2', function () {
        const page = structuredClone(notifications);
        page.results = notifications.results.slice(0, 2);
        page.unread_count = page.results.filter(n => n.state !== "READ_STATE").length;
        return page;
      })
      .get('/?limit=4', function () {
        const page = structuredClone(notifications);
        page.next = null;
        page.unread_count = page.results.filter(n => n.state !== "READ_STATE").length;
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

  return {
    components: {NotificationViewer},
    template: `
      <ul class="nav navbar-nav">
      <NotificationViewer baseUrl="/" :interval="10" :limit="2" />
      </ul>
    `,
  };
};

export const WithErrors: StoryFn<typeof NotificationViewer> = () => {
  fetchMock.restore()
      .get('/?limit=15', mockNotifications)
      .put('/mark_all_as_read', 500)
      .patch('*', {throws: new Error('Network error')});

  return {
    components: {NotificationViewer},
    template: `
      <ul class="nav navbar-nav">
      <NotificationViewer baseUrl="/" :interval="10" />
      </ul>
    `,
  };
};

export default {
  title: 'Global component',
  component: NotificationViewer,
} as Meta<typeof NotificationViewer>;
