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

    def get(self, request) -> Response:
        queryset = Contractor.objects.all()
        serializer = ContractorSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)

    def post(self, request) -> Response:
        response = {"data": None,
                    "success": False}
        data = request.data.get("data")
        if not data:
            return Response(response)
        serializer = ContractorSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer = ContractorSerializer.create_or_update_from_data(
                validated_data=data)
            response = {"data": serializer.data,
                        "success": True}
        return Response(response)


class OrderView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)
