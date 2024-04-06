from rest_framework import serializers
from warehouse_app.serializers import CargoSerializer
from order_app.models import (
    Contractor,
    Order
)


class ContractorSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=150, allow_blank=True)
    address1 = serializers.CharField(max_length=255, allow_blank=True)
    address2 = serializers.CharField(max_length=255, allow_blank=True)
    address3 = serializers.CharField(max_length=255, allow_blank=True)
    phone1 = serializers.CharField(max_length=25, allow_blank=True)
    phone2 = serializers.CharField(max_length=25, allow_blank=True)
    phone3 = serializers.CharField(max_length=25, allow_blank=True)

    def create(self, validated_data):
        return Contractor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "id":
                continue
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def create_or_update_from_data(validated_data):
        data = []
        for item in validated_data:
            id = item.get("id")
            if id:
                contractor = Contractor.objects.get(id=id)
                contractor = ContractorSerializer(contractor, data=item)
            else:
                contractor = ContractorSerializer(data=item)
            contractor.is_valid(raise_exception=True)
            contractor.save()
            data.append(contractor.instance)
        serializer = ContractorSerializer(data=data, many=True)
        serializer.is_valid()
        return serializer


class OrderSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    number = serializers.IntegerField(required=False)
    date = serializers.DateTimeField()
    sender = ContractorSerializer()
    sender_name = serializers.CharField(max_length=150, allow_blank=True)
    sender_address = serializers.CharField(max_length=255, allow_blank=True)
    sender_phone = serializers.CharField(max_length=25, allow_blank=True)
    recipient = ContractorSerializer()
    recipient_name = serializers.CharField(max_length=150, allow_blank=True)
    recipient_address = serializers.CharField(max_length=255, allow_blank=True)
    recipient_phone = serializers.CharField(max_length=25, allow_blank=True)
    cargos = CargoSerializer(many=True)


class CreateUpdateOrderSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    number = serializers.IntegerField(required=False)
    date = serializers.DateTimeField()
    sender_id = serializers.UUIDField()
    sender_name = serializers.CharField(max_length=150, allow_blank=True)
    sender_address = serializers.CharField(max_length=255, allow_blank=True)
    sender_phone = serializers.CharField(max_length=25, allow_blank=True)
    recipient_id = serializers.UUIDField()
    recipient_name = serializers.CharField(max_length=150, allow_blank=True)
    recipient_address = serializers.CharField(max_length=255, allow_blank=True)
    recipient_phone = serializers.CharField(max_length=25, allow_blank=True)

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.sender = Contractor.objects.get(
            id=validated_data.get("sender_id"))
        order.recipient = Contractor.objects.get(
            id=validated_data.get("recipient_id"))
        return order

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "id":
                continue
            if hasattr(instance, key):
                setattr(instance, key, value)
            if key == "sender_id":
                instance.sender = Contractor.objects.get(
                    id=value)
            if key == "recipient_id":
                instance.recipient = Contractor.objects.get(
                    id=value)
        instance.save()
        return instance

    @staticmethod
    def create_or_update_from_data(validated_data):
        data = []
        for item in validated_data:
            id = item.get("id")
            if id:
                contractor = Order.objects.get(id=id)
                contractor = CreateUpdateOrderSerializer(contractor, data=item)
            else:
                contractor = CreateUpdateOrderSerializer(data=item)
            contractor.is_valid(raise_exception=True)
            contractor.save()
            data.append(contractor.instance)
        serializer = OrderSerializer(data=data, many=True)
        serializer.is_valid()
        return serializer
