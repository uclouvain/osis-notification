from rest_framework import serializers

from osis_notification.models import WebNotification


class WebNotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    sent_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    read_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M')

    class Meta:
        model = WebNotification
        fields = [
            "uuid",
            "state",
            "payload",
            "created_at",
            "sent_at",
            "read_at",
        ]
