# ##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2022 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
# ##############################################################################
from django.urls import path as _path

from osis_notification.api.utils import proxy_view
from osis_notification.api.views import (
    MarkAllNotificationsAsReadView,
    MarkNotificationAsReadView,
    SentNotificationListView,
)


def proxy_path(pattern, view, name=None):
    name = getattr(view, 'name', name)
    view = proxy_view(view)
    return _path(pattern, view, name=name)


app_name = "osis_notification"
urlpatterns = [
    proxy_path("", SentNotificationListView),
    proxy_path("mark_all_as_read", MarkAllNotificationsAsReadView),
    proxy_path("<uuid:notification_uuid>", MarkNotificationAsReadView),
]
