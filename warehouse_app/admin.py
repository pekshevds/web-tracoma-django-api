from django.contrib import admin
from warehouse_app.models import (
    Cargo,
    Warehouse,
    Incoming,
    IncomingItem,
    Outgoing,
    OutgoingItem,
    Moving,
    MovingItem,
    CargoRegistry
)


@admin.register(CargoRegistry)
class CargoRegistryAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "period", "register",
                    "cargo", "warehouse", "quant",)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("__str__", "type", "id",)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "id",)


class CargoInLine(admin.TabularInline):
    model = Cargo
    fields = ("name",)


class IncomingItemInLine(admin.TabularInline):
    model = IncomingItem
    fields = ("incoming", "cargo",)


@admin.register(Incoming)
class IncomingAdmin(admin.ModelAdmin):
    inlines = [IncomingItemInLine]
    list_display = ("__str__", "id",)


class OutgoingItemInLine(admin.TabularInline):
    model = OutgoingItem
    fields = ("outgoing", "cargo",)


@admin.register(Outgoing)
class OutgoingAdmin(admin.ModelAdmin):
    inlines = [OutgoingItemInLine]
    list_display = ("__str__", "id",)


class MovingItemInLine(admin.TabularInline):
    model = MovingItem
    fields = ("moving", "cargo",)


@admin.register(Moving)
class MovingAdmin(admin.ModelAdmin):
    inlines = [MovingItemInLine]
    list_display = ("__str__", "id",)
