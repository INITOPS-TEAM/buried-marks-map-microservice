from rest_framework.permissions import BasePermission

MAP_ALLOWED_ROLES = ['viewer', 'editor', 'admin']

class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user_role in ['editor', 'admin']

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user_role == 'admin'

class HasMapAccess(BasePermission):
    def has_permission(self, request, view):
        return request.user_role in MAP_ALLOWED_ROLES
