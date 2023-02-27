from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViews(APIView):
    def create_user(self, serializer):
        serializer.save()

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.create_user(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def get(self, request, user_id):
        find_user = self.get_user(user_id)
        serializer = UserSerializer(find_user)

        if request.user == find_user or request.user.is_superuser:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, user_id):
        find_user = self.get_user(user_id)
        serializer = UserSerializer(find_user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        if request.user == find_user or request.user.is_superuser:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)