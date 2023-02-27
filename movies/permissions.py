from rest_framework.views import Request, View
from rest_framework import permissions

from .models import Movie

class CheckProperty(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, movie: Movie):
        return movie.added_by == request.user