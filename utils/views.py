from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import Token
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
<<<<<<< HEAD
from django.middleware import csrf
from typing import override
=======
from typing import override, Dict
from user.models import User


def get_user_data(token: Token) -> Dict[str, str]:
    """ get user info by Token """
    auth = JWTAuthentication()
    user: User = auth.get_user(token)  # type: ignore
    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.get_full_name(),
        'email': user.email,
    }
    return user_data
>>>>>>> 4c4dd1776e23cf9e64b5ffb189f6e2cee1434954


class CustomTokenObtainPairView(TokenObtainPairView):
    @override
    def post(self, request: Request, *args, **kwargs) -> Response:
        super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
<<<<<<< HEAD
        csrf.get_token(request)
        response = Response({'access': data['access']}, status.HTTP_200_OK)
=======
        token = data['access']
        user_data = get_user_data(token)
        response = Response(
            {
                'access': token,
                'user': user_data,
            },
            status.HTTP_200_OK)
>>>>>>> 4c4dd1776e23cf9e64b5ffb189f6e2cee1434954
        response.set_cookie(
            key='token_refresh',
            value=data.get('refresh'),
            httponly=True,
            samesite='Strict',
        )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    @override
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        data["refresh"] = request.COOKIES.get('token_refresh', 'invalid token')
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
