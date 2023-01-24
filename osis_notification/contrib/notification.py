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

from typing import Union

from base.models.person import Person


class EmailNotification(object):
    def __init__(
        self,
        recipient: Union[Person, str],
        subject: str,
        plain_text_content: str,
        html_content: str,
    ):
        """This class must be implemented in order to use the email notification
        handlers.

        :param recipient: Represent the notification's recipient and must be a Person
        instance or an email.
        :param subject: The subject of the email notification.
        :param plain_text_content: Represent the plain text content of the notification.
        :param html_content: Represent the html content of the notification."""

        self.recipient = recipient
        self.subject = subject
        self.plain_text_content = plain_text_content
        self.html_content = html_content


class WebNotification(object):
    def __init__(self, recipient: Person, content: str):
        """This class must be implemented in order to use the web notification handlers.

        :param recipient: Represent the notification's recipient and must be a Person
        instance.
        :param content: Represent the content of the notification."""

        self.recipient = recipient
        self.content = content
