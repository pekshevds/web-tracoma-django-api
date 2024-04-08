from django.http import HttpRequest
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_app.models import User
from auth_app.serializers import UserSerializer
from auth_app.transport import send_pin_code, fetch_recipient
from auth_app.services import (
    add_pin,
    authenticate,
    update_or_create_user_token,
    use_pin_code
)


class UserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        username = request.GET.get("username", None)
        if username:
            queryset = User.objects.filter(username=username)
            serializer = UserSerializer(queryset, many=True)
        else:
            queryset = User.objects.filter(is_superuser=False)
            serializer = UserSerializer(queryset, many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)


class UserInfoView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        serializer = UserSerializer([request.user], many=True)
        response = {"data": serializer.data,
                    "success": True}
        return Response(response)


class PinView(APIView):
    """Отправляет pin для существующего пользователя.
    Пользователь определяется по имени (номеру телефона)
     или адресу электронной почты.
    Порядок получения пользователя определяется в настройках.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request: HttpRequest) -> Response:
        recipient = request.GET.get("recipient")
        success = False
        if recipient:
            user = fetch_recipient(recipient)
            if user:
                pin = add_pin(user)
                send_pin_code(pin.pin_code, recipient)
                success = True
        return Response({"data": None,
                         "success": success})


class TokenView(APIView):
    """Возвращает токен по имени пользователя и актуальному пину.
    Пользователь определяется по имени (номеру телефона)
     или адресу электронной почты.
    Порядок получения пользователя определяется в настройках.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest) -> Response:
        username = request.POST.get("username")
        pincode = request.POST.get("pincode")
        user = authenticate(username, pincode)
        if user is not None:
            token = update_or_create_user_token(user=user)
            if token is not None:
                use_pin_code(pincode)
                return Response({"data": {
                    "token": token.key
                },
                    "success": True})
        return Response({"data": None,
                         "success": False})
