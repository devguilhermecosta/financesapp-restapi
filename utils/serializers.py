from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from typing import override, Dict, Any
from utils.views import get_user_data


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
