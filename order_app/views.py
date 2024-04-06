from django.http import HttpRequest
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from main_app.services import fetch_queryset_from_request_data
from order_app.models import (
    Contractor,
    Order
)
from order_app.serializers import (
    ContractorSerializer,
    CreateUpdateOrderSerializer,
    OrderSerializer
)


class ContractorView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        queryset = fetch_queryset_from_request_data(request, Contractor)
        serializer = ContractorSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)

    def post(self, request: HttpRequest) -> Response:
        response = {"data": None,
                    "success": False}
        data = request.data.get("data")
        if not data:
            return Response(response)
        serializer = ContractorSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer = ContractorSerializer.create_or_update_from_data(data)
            response = {"data": serializer.data,
                        "success": True}
        return Response(response)


class OrderView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        queryset = fetch_queryset_from_request_data(request, Order)
        serializer = OrderSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)

    def post(self, request: HttpRequest) -> Response:
        response = {"data": None,
                    "success": False}
        data = request.data.get("data")
        if not data:
            return Response(response)
        serializer = CreateUpdateOrderSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer = CreateUpdateOrderSerializer.create_or_update_from_data(data)
            response = {"data": serializer.data,
                        "success": True}
        return Response(response)
