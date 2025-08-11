from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access to all users, but write access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsOwnerOrAdmin(BasePermission):
    """
    Allows access only to the owner of the resource or admin users.
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            (request.user.is_staff or
             (hasattr(obj, 'user') and obj.user == request.user))
        )