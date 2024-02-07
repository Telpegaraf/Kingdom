from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwner(BasePermission):
    """
    Users can edit only their characters
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'character'):
            return obj.character.user == request.user or IsAdminUser().has_permission(request, view)
        if hasattr(obj, 'bag') and hasattr(obj.bag, 'character'):
            return obj.bag.character.user == request.user or IsAdminUser().has_permission(request, view)
        else:
            return obj.user == request.user or IsAdminUser().has_permission(request, view)
