from rest_framework import serializers
from .models import Receive
from user.models import User


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
