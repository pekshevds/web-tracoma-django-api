from rest_framework import serializers
from warehouse_app.serializers import CargoSerializer


class ContractorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=150)
    address1 = serializers.CharField(max_length=255)
    address2 = serializers.CharField(max_length=255)
    address3 = serializers.CharField(max_length=255)
    phone1 = serializers.CharField(max_length=25)
    phone2 = serializers.CharField(max_length=25)
    phone3 = serializers.CharField(max_length=25)


class OrderSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    number = serializers.IntegerField()
    date = serializers.DateTimeField()
    sender = ContractorSerializer()
    sender_name = serializers.CharField(max_length=150)
    sender_address = serializers.CharField(max_length=255)
    sender_phone = serializers.CharField(max_length=25)
    recipient = ContractorSerializer()
    recipient_name = serializers.CharField(max_length=150)
    recipient_address = serializers.CharField(max_length=255)
    recipient_phone = serializers.CharField(max_length=25)
    cargos = CargoSerializer(many=True)
