from django.utils.translation import gettext_lazy as _

from base.models.utils.utils import ChoiceEnum


class NotificationStates(ChoiceEnum):
    PENDING_STATE = _("Pending")
    SENT_STATE = _("Sent")
    READ_STATE = _("Read")


class NotificationTypes(ChoiceEnum):
    EMAIL_TYPE = _("Email notification")
    WEB_TYPE = _("Web notification")
