from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import override, Dict, Any


class CustomTokenObtainPairView(TokenObtainPairView):
    @override
    def post(self, request: Request, *args, **kwargs) -> Response:
        super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = Response({'access': data['access']}, status.HTTP_200_OK)
        response.set_cookie(
            key='token_refresh',
            value=data.get('refresh'),
            httponly=True,
        )

        return response


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    @override
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        data = {"access": str(refresh.access_token)}
        return data


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        data["refresh"] = request.COOKIES.get('token_refresh', 'invalid token')
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
