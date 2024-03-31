from rest_framework import serializers


class WarehouseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=150)
    type = serializers.CharField(max_length=2)


class CargoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=150)
    order_id = serializers.UUIDField()
    width = serializers.DecimalField(max_digits=15, decimal_places=3)
    height = serializers.DecimalField(max_digits=15, decimal_places=3)
    length = serializers.DecimalField(max_digits=15, decimal_places=3)
    weight = serializers.DecimalField(max_digits=15, decimal_places=3)
    volume = serializers.DecimalField(max_digits=15, decimal_places=5)
    description = serializers.CharField(max_length=150)
