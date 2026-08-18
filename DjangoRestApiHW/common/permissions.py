from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return False
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_staff
