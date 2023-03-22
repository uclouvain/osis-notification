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
/* eslint-disable vue/prefer-import-from-vue */
import {createApp} from '@vue/runtime-dom'; // to allow to be spied on
import NotificationViewer from './NotificationViewer.vue';
import {i18n} from './i18n';

interface Props extends Record<string, unknown> {
  baseUrl: string,
  interval?: number,
  limit?: number,
  truncateLength?: number,
}

document.querySelectorAll<HTMLElement>('#notification-viewer').forEach((elem) => {
  const props: Props = {baseUrl: "", ...elem.dataset};
  if (elem.dataset.interval) {
    props.interval = Number.parseInt(elem.dataset.interval);
  }
  if (elem.dataset.limit) {
    props.limit = Number.parseInt(elem.dataset.limit);
  }
  if (elem.dataset.truncateLength) {
    props.truncateLength = Number.parseInt(elem.dataset.truncateLength);
  }
  createApp(NotificationViewer, props).use(i18n).mount(elem);
});
