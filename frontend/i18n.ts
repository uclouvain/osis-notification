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

import {createI18n} from 'vue-i18n';

const messages = {
  en: {
    notification_viewer: {
      mark_all_as_read: 'Mark all as read',
      error: 'An error occurred, please try again later.',
      load_more: 'Load more',
      loading: 'Loading...',
      no_notifications: 'No notifications.',
    },
    notification: {
      mark_as_read: 'Mark as read',
      mark_as_unread: 'Mark as unread',
      show_less: 'Show less',
      show_more: 'Show more',
    },
  },
  'fr-be': {
    notification_viewer: {
      mark_all_as_read: 'Tout marquer comme lu',
      error: 'Une erreur s\'est produite, veuillez réessayer plus tard.',
      load_more: 'Afficher plus',
      loading: 'Chargement...',
      no_notifications: 'Pas de notifications.',
    },
    notification: {
      mark_as_read: 'Marquer comme lu',
      mark_as_unread: 'Marquer comme non-lu',
      show_less: 'Voir moins',
      show_more: 'Voir plus',
    },
  },
};
export const i18n = createI18n({
  locale: document.documentElement.lang || 'en',
  messages,
});
