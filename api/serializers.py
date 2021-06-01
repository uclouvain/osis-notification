from rest_framework import serializers

from osis_notification.models import WebNotification


class WebNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebNotification
        fields = [
            "payload",
            "created_at",
            "sent_at",
        ]
