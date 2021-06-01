from rest_framework import permissions


class IsNotificationRecipient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.person.uuid == view.kwargs["uuid"]