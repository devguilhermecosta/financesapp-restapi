from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer


class UserMixin:
    def get_object(self, pk: int) -> User:
        user = get_object_or_404(
            User,
            pk=pk
        )
        return user


class UserRegisterAPIView(APIView, UserMixin):
    def get_object(self, pk: int) -> User:
        user = get_object_or_404(
            User,
            pk=pk
        )
        self.check_object_permissions(self.request, user)
        return user

    def post(self, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_id = serializer.data.get('id', None)
        user_data = self.request.data

        user = self.get_object(user_id)
        user.set_password(user_data.get('password'))
        user.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserDetailAPIView(APIView, UserMixin):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        user = self.get_object(kwargs.get('id', None))
        serializer = UserSerializer(instance=user)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, *args, **kwargs) -> Response:
        user = self.get_object(kwargs.get('id', None))
        data = self.request.data
        data_filter = {key: val for key, val in data.items() if key != 'email'}
        serializer = UserSerializer(user, data=data_filter, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    def delete(self, *args, **kwargs) -> Response:
        user = self.get_object(kwargs.get('id', None))
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(
            instance=users,
            many=True
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
