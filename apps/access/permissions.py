from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    message = ""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and hasattr(user, "role")
            and user.role.name == "admin"
        )
