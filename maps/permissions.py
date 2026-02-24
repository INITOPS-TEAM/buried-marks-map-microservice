from rest_framework.permissions import BasePermission
# 1 - viewer; 2 - editor (silver); 3 - admin (gold)
MAP_ALLOWED_ROLES = ["1", "2", "3"]

class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user_role in ["2", "3"]

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user_role == "3"

class HasMapAccess(BasePermission):
    def has_permission(self, request, view):
        return request.user_role in MAP_ALLOWED_ROLES
