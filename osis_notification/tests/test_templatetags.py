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
from django.template import Context, Template
from django.test import TestCase, override_settings
from django.urls import include, path

urlpatterns = [path('foo/', include('osis_notification.urls'))]


@override_settings(ROOT_URLCONF=__name__, OSIS_NOTIFICATION_BASE_URL="/")
class TemplateTagTestCase(TestCase):
    def test_template_tag(self):
        rendered = Template('{% load osis_notification %}{% notification_viewer %}').render(context=Context())
        self.assertEqual('<div id="notification-viewer" data-base-url="/foo/"></div>', rendered)

        rendered = Template('{% load osis_notification %}{% notification_viewer limit=20 %}').render(context=Context())
        self.assertEqual('<div id="notification-viewer" data-base-url="/foo/" data-limit="20"></div>', rendered)
