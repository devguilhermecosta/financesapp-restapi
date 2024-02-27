from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import AbstractBaseUser

from .serializers import ReceiveSerializer
from .models import Receive


def get_user_by_token(token: bytes) -> AbstractBaseUser:
    auth = JWTAuthentication()
    access_token = auth.get_validated_token(token)
    user = auth.get_user(access_token)
    return user


def get_token_from_header(request: Request) -> bytes:
    token = request.headers['Authorization'].replace('Bearer ', '')
    return token


def get_user(request: Request) -> AbstractBaseUser:
    token = get_token_from_header(request)
    user = get_user_by_token(token)
    return user


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        user = get_user(self.request)
        date = self.request.data.get('date', None)

        if date is not None:
            data = get_list_or_404(
                Receive,
                user_id=user.pk,
                date=date,
            )

            receipt = sum([d.value for d in data if d.type == 'receipt'])
            expense = sum([d.value for d in data if d.type == 'expense'])

            report = [
                {
                    "tag": "balance",
                    "value": receipt - expense
                },
                {
                    "tag": "receipt",
                    "value": receipt,
                },
                {
                    "tag": "expense",
                    "value": expense,
                }
            ]

            return Response(
                data=report,
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"details": "date is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ReceiveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs) -> Response:
        user = get_user(self.request)

        data = self.request.data
        data['user'] = user.pk

        serializer = ReceiveSerializer(
            data=data,
            many=False
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, *args, **kwargs) -> Response:
        receive_id = self.request.data.get('receive_id', None)

        if not receive_id:
            return Response(
                data={"detail": "receive_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        receive = get_object_or_404(
            Receive,
            id=receive_id
        )
        receive.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class ReceiveList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        user = get_user(self.request)
        date = self.request.data.get('date', None)

        if date is not None:
            data = get_list_or_404(
                Receive.objects.order_by('-id'),
                user_id=user.pk,
                date=date
            )

            serializer = ReceiveSerializer(
                instance=data,
                many=True
            )

            return Response(
                serializer.data,
                status.HTTP_200_OK
            )

        return Response(
            data={"details": "date is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
