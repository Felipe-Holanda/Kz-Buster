from rest_framework.views import Request, View
from rest_framework import permissions

class UserPropertyCheck(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: object):
        return request.user.is_authenticated and user == request.user or request.user.is_superuser
    
class CheckPrivilleges(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
        )