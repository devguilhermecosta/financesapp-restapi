from rest_framework import serializers
from .models import Receive
from user.models import User


TYPES_OF_MOVEMENTS = [
    'expense',
    'receipt',
]


class ReceiveSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Receive
        fields = [
            'id',
            'user',
            'description',
            'value',
            'type',
            'date',
        ]

    def validate_type(self, value: str) -> str:
        if value not in TYPES_OF_MOVEMENTS:
            raise serializers.ValidationError(
                "type not allowed. Use 'expense' or 'receipt'"
            )

        return value
