from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ReceiveSerializer
from .models import Receive
from django.shortcuts import get_list_or_404


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        user_id = self.request.data.get('user_id', None)
        date = self.request.data.get('date', None)

        if (user_id is not None and date is not None):
            data = get_list_or_404(
                Receive,
                user_id=user_id
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
            data={"details": "user_id and date is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ReceiveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs) -> Response:
        serializer = ReceiveSerializer(
            data=self.request.data,
            many=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=self.request.data,
            status=status.HTTP_201_CREATED,
        )


class ReceiveList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        user_id = self.request.data.get('user_id', None)
        date = self.request.data.get('date', None)

        if (user_id is not None and date is not None):
            data = get_list_or_404(
                Receive,
                user_id=user_id,
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
            data={"details": "user_id and date is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
