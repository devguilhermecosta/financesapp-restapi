from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


class UserListAPIView(APIView):
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
