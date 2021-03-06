import NotificationViewer from './NotificationViewer';
import fetchMock from 'fetch-mock';


const mockNotifications = {
  count: 3,
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

if (process.env.NODE_ENV === 'test') {
  // Mock jQuery for snapshots tests
  window.jQuery = jest.fn(() => ({
    on: () => {},
    tooltip: () => {},
  }));
}

export const noNotification = () => {
  fetchMock.restore().get('/?limit=15', {count: 0, results: []});
  return {
    components: { NotificationViewer },
    template: `
      <ul class="nav navbar-nav">
      <NotificationViewer baseUrl="/" />
      </ul>
    `,
  };
};

export const withNotifications = () => {
  let currentNotificationPage = {...mockNotifications};
  fetchMock.restore()
    .get('/?limit=2', function() {
      currentNotificationPage.results = mockNotifications.results.slice(0, 2);
      return currentNotificationPage;
    })
    .get('/?limit=4',  function() {
      currentNotificationPage.results = mockNotifications.results;
      delete currentNotificationPage.next;
      return currentNotificationPage;
    })
    .put('/mark_all_as_read', function () {
      currentNotificationPage.results.forEach(notification => {
        notification.state = 'READ_STATE';
        notification.read_at = Date.now();
      });
      return currentNotificationPage.results;
    })
    .patch('*', function (url) {
      let notification = currentNotificationPage.results.find(n => url.includes(n.uuid));
      notification.state = (notification.state === "READ_STATE") ? "SENT_STATE" : "READ_STATE";
      notification.read_at = (notification.state === "READ_STATE") ? Date.now() : null;
      return notification;
    });

  return {
    components: { NotificationViewer },
    template: `
      <ul class="nav navbar-nav">
      <NotificationViewer baseUrl="/" :interval="500" :limit="2" />
      </ul>
    `,
  };
};

export const withErrors = () => {
  fetchMock.restore()
    .get('/?limit=15', mockNotifications)
    .put('/mark_all_as_read', {throws: { statusText: 'Network error'}})
    .patch('*', {throws: { statusText: 'Network error'}});

  return {
    components: { NotificationViewer },
    template: `
      <ul class="nav navbar-nav">
      <NotificationViewer baseUrl="/" :interval="10" />
      </ul>
    `,
  };
};

export default {
  title: 'Global component',
};
