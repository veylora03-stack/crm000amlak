from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, 'role', None) == 'Admin')
        )


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)

        return bool(
            request.user and
            request.user.is_authenticated and
            (
                request.user.is_staff or
                role in ['Admin', 'Manager']
            )
        )


class IsAgentOrAbove(BasePermission):
    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)

        return bool(
            request.user and
            request.user.is_authenticated and
            role in ['Admin', 'Manager', 'Agent']
        )
