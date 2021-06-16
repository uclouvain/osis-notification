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

import { getCookie } from './utils.js';

describe('cookies are not set', () => {
  it('should return null', () => {
    delete window.document.cookie;
    expect(getCookie('csrf')).toEqual(null);
  });
});

describe('cookies are set', () => {
  it('should return the asked cookie', () => {
    Object.defineProperty(window.document, 'cookie', {
      writable: true,
      value: 'csrf=1234-5678-9101-1121-3141;anotherCookie=value',
    });
    expect(getCookie('csrf')).toEqual('1234-5678-9101-1121-3141');
    expect(getCookie('anotherCookie')).toEqual('value');
    expect(getCookie('thisCookieDoesNotExists')).toEqual(null);
  });
});
