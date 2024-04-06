from rest_framework import serializers
from warehouse_app.serializers import CargoSerializer
from order_app.models import Contractor


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
        for key in validated_data.keys():
            if key == "id":
                continue
            if hasattr(instance, key):
                setattr(instance, key,
                        validated_data.get(key, getattr(instance, key))
                        )
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
