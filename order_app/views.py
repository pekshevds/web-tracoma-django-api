from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from order_app.models import (
    Contractor,
    Order
)
from order_app.serializers import (
    ContractorSerializer,
    OrderSerializer
)


class ContractorView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def get(self, request) -> Response:
        queryset = Contractor.objects.all()
        serializer = ContractorSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)


class OrderView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def get(self, request) -> Response:
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)
