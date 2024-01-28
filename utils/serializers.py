from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from user.models import User
from typing import override, Dict, Any


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


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    @override
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        user_data = get_user_data(refresh)
        data = {
            "access": str(refresh.access_token),
            "user": user_data,
        }

        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @override
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        token = self.token_class(data['refresh'])  # type: ignore
        user_data = get_user_data(token)
        data['user'] = user_data  # type: ignore
        return data
