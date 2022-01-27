from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser
from users.models import User


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, User):
            return True
        else:
            return False


class AllowRetriveList(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True

        return False
