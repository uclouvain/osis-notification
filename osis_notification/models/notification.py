# ##############################################################################
#
#  OSIS stands for Open Student Information System. It's an application
#  designed to manage the core business of higher education institutions,
#  such as universities, faculties, institutes and professional schools.
#  The core business involves the administration of students, teachers,
#  courses, programs and so on.
#
#  Copyright (C) 2015-2023 Université catholique de Louvain (http://www.uclouvain.be)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  A copy of this license - GNU General Public License - is available
#  at the root of the source code of this program.  If not,
#  see http://www.gnu.org/licenses/.
#
# ##############################################################################

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.person import Person
from osis_notification.models.enums import (
    NotificationStates,
    NotificationTypes,
)


class Notification(models.Model):
    """Base class for a notification"""

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    type = models.CharField(
        _("Type"),
        choices=NotificationTypes.choices(),
        max_length=25,
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )
    payload = models.TextField(_("Payload"))
    state = models.CharField(
        _("State"),
        choices=NotificationStates.choices(),
        default=NotificationStates.PENDING_STATE.name,
        max_length=25,
    )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    sent_at = models.DateTimeField(verbose_name=_("Sent at"), editable=False, null=True)
    read_at = models.DateTimeField(verbose_name=_("Read at"), editable=False, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # A person cannot be null for WEB type
                check=~models.Q(
                    type=NotificationTypes.WEB_TYPE.name,
                    person_id__isnull=True,
                ),
                name='person_required_for_web',
            ),
        ]
        ordering = ["-created_at"]
