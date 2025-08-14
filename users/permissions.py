from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminRole(BasePermission):
    """
    Allows access only to users with role=admin or staff/superuser.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "role", "citizen") == "admin" or user.is_staff or user.is_superuser

class ReadOnlyOrAdmin(BasePermission):
    """
    Citizens can read; only admins can write.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and (
            getattr(user, "role", "citizen") == "admin" or user.is_staff or user.is_superuser
        ))
