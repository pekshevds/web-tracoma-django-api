from django.http import HttpRequest
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from main_app.services import fetch_queryset_from_request_data
from warehouse_app.models import (
    Warehouse,
    Cargo
)
from warehouse_app.serializers import (
    WarehouseSerializer,
    CargoSerializer
)


class WarehouseView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        queryset = fetch_queryset_from_request_data(request, Warehouse)
        serializer = WarehouseSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)


class CargoView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        queryset = fetch_queryset_from_request_data(request, Cargo)
        serializer = CargoSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)

    def post(self, request: HttpRequest) -> Response:
        response = {"data": None,
                    "success": False}
        data = request.data.get("data")
        if not data:
            return Response(response)
        serializer = CargoSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer = CargoSerializer.create_or_update_from_data(data)
            response = {"data": serializer.data,
                        "success": True}
        return Response(response)
