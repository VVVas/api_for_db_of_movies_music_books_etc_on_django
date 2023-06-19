from rest_framework.permissions import SAFE_METHODS, BasePermission

from .messages import (PERMISSION_ADMIN_EDIT, PERMISSION_ADMIN_USE,
                       PERMISSION_EDIT)


class IsAdmin(BasePermission):
    message = PERMISSION_ADMIN_USE

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAdminOrReadOnly(BasePermission):
    message = PERMISSION_ADMIN_EDIT

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin or request.user.is_superuser)))


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    message = PERMISSION_EDIT

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user or request.user.is_moderator
            or request.user.is_admin or request.user.is_superuser
        )
