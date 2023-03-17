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

import {expect, test, vi} from 'vitest';
/* eslint-disable vue/prefer-import-from-vue */
import * as exports from '@vue/runtime-dom';
import fetchMock from "fetch-mock";
import {createApp} from "vue";
import type {EntriesResponse} from "./interfaces";

const jQueryMock = vi.fn(() => ({
  on: vi.fn(),
  tooltip: vi.fn(),
}));

vi.stubGlobal('jQuery', jQueryMock);
fetchMock.reset().mock('path:/api', {
  results: [],
  count: 0,
  unread_count: 0,
  next: null,
  previous: null,
} as EntriesResponse);

const spy = vi.spyOn(exports, 'createApp').mockImplementation(createApp);

test('with url ', async () => {
  window.document.cookie = 'csrftoken=1234-5678-9101-1121-3141';
  document.body.innerHTML = `<div id="notification-viewer" data-base-url="/api"></div>`;

  // Executes main file
  await import('./main');
  expect(document.body.innerHTML).toMatchSnapshot();

  const pElement = document.querySelectorAll('[data-v-app]');
  expect(pElement).toHaveLength(1);

  expect(spy.mock.calls[0][1]).toStrictEqual({
    baseUrl: '/api',
  });
});


test('app with conversions', async () => {
  vi.resetModules();
  spy.mockClear();
  window.document.cookie = 'csrftoken=1234-5678-9101-1121-3141';
  document.body.innerHTML = `
    <div id="notification-viewer" data-base-url="/api" data-limit="3" data-interval="10" data-truncate-length="50"></div>
  `;

  // Executes main file
  await import('./main');

  expect(spy.mock.calls[0][1]).toStrictEqual({
    baseUrl: '/api',
    limit: 3,
    interval: 10,
    truncateLength: 50,
  });
});
