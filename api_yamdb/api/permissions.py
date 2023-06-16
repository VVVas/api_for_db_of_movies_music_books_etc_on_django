from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    message = 'Использовать контент может только администратор.'

    def has_permission(self, request, view):
        return (request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    message = 'Изменить контент может только администратор.'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_superuser)))


class IsModeratorOrReadOnly(BasePermission):
    message = 'Изменить контент может только модератор.'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_moderator))


class IsAuthorOrReadOnly(BasePermission):
    message = 'Изменить контент может только автор.'

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
