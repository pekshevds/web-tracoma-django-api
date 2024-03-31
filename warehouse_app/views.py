from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from warehouse_app.models import (
    Warehouse,
    Cargo
)
from warehouse_app.serializers import (
    WarehouseSerializer,
    CargoSerializer
)


class WarehouseView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request) -> Response:
        queryset = Warehouse.objects.all()
        serializer = WarehouseSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)


class CargoView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def get(self, request) -> Response:
        queryset = Cargo.objects.all()
        serializer = CargoSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)
