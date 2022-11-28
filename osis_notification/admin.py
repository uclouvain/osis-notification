from django.contrib import admin
from osis_notification.models import Notification
from osis_notification.models.enums import NotificationTypes, NotificationStates
from osis_notification.contrib.handlers import EmailNotificationHandler, WebNotificationHandler


@admin.action(description='Send selected pending notifications')
def send_pending_notification(modeladmin, request, queryset):
    for pending_notification in queryset.filter(state=NotificationStates.PENDING_STATE.name):
        if pending_notification.type == NotificationTypes.WEB_TYPE.name:
            WebNotificationHandler.process(pending_notification)
        elif pending_notification.type == NotificationTypes.EMAIL_TYPE.name:
            EmailNotificationHandler.process(pending_notification)


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'type',
        'person',
        'state',
        'created_at',
    )
    list_filter = (
        'type',
        'state',
    )
    search_fields = (
        'uuid',
        'person__global_id',
        'person__first_name',
        'person__last_name',
    )
    raw_id_fields = ('person',)
    date_hierarchy = 'created_at'
    actions = [send_pending_notification]


admin.site.register(Notification, NotificationAdmin)
