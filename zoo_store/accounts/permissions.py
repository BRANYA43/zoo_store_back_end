from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    # def has_permission(self, request, view):
    #     return bool(request.user.is_authenticated or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return request.user.uuid == obj.user.uuid
        return request.user.uuid == obj.uuid


class IsOwnerOrStaff(IsOwner):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.uuid == obj.uuid or request.user.is_staff)
