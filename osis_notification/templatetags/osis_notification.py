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
from django import template
from django.shortcuts import resolve_url
from django.utils.html import escapejs
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def notification_viewer(**kwargs):
    attrs = {'data-base-url': resolve_url("osis_notification:notification-list")}
    for name, value in kwargs.items():
        attrs['data-' + "-".join(name.lower().split("_"))] = escapejs(value)
    return mark_safe(
        '<li id="notification-viewer" class="dropdown nav-item" {}></li>'.format(
            " ".join('{}="{}"'.format(k, v) for k, v in attrs.items()),
        )
    )
