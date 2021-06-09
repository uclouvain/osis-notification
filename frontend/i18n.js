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

import Vue from 'vue';
import VueI18n from 'vue-i18n';

Vue.use(VueI18n);

const messages = {
  en: {
    mark_all_as_read: 'Mark all as read',
    mark_as_read: 'Mark as read',
    mark_as_unread: 'Mark as unread',
    error_mark_as_read: 'An error occurred while marking the notification as read, please try again later.',
    error_mark_all_as_read: 'An error occurred while marking all the notifications as read, please try again later.',
  },
  'fr-be': {
    mark_all_as_read: 'Tout marquer comme lu',
    mark_as_read: 'Marquer comme lu',
    mark_as_unread: 'Marquer comme non-lu',
    error_mark_as_read: 'Une erreur s\'est produite lors du marquage de la notification comme lue, veuillez réessayer plus tard.',
    error_mark_all_as_read: 'Une erreur s\'est produite lors du marquage des notifications comme lues, veuillez réessayer plus tard.',
  },
};
export const i18n = new VueI18n({
  locale: document.documentElement.lang || 'en',
  messages,
});