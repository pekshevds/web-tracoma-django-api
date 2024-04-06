from rest_framework import serializers
from warehouse_app.models import Cargo
from order_app.models import Order


class WarehouseSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=150)
    type = serializers.CharField(max_length=2)


class CargoSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=150)
    order_id = serializers.UUIDField(read_only=True)
    width = serializers.DecimalField(max_digits=15, decimal_places=3)
    height = serializers.DecimalField(max_digits=15, decimal_places=3)
    length = serializers.DecimalField(max_digits=15, decimal_places=3)
    weight = serializers.DecimalField(max_digits=15, decimal_places=3)
    volume = serializers.DecimalField(max_digits=15, decimal_places=5)
    description = serializers.CharField(max_length=150, allow_blank=True)

    def create(self, validated_data):
        cargo = Cargo.objects.create(**validated_data)
        cargo.order = Order.objects.get(id=validated_data.get("order_id"))
        return cargo

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "id":
                continue
            if hasattr(instance, key):
                setattr(instance, key, value)
            if key == "order_id":
                instance.sender = Cargo.objects.get(
                    id=value)
        instance.save()
        return instance

    @staticmethod
    def create_or_update_from_data(validated_data):
        data = []
        for item in validated_data:
            id = item.get("id")
            if id:
                cargo = Cargo.objects.get(id=id)
                cargo = CargoSerializer(cargo, data=item)
            else:
                cargo = CargoSerializer(data=item)
            cargo.is_valid(raise_exception=True)
            cargo.save()
            data.append(cargo.instance)
        serializer = CargoSerializer(data=data, many=True)
        serializer.is_valid()
        return serializer
