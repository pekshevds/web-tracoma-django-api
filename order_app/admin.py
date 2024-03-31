from django.contrib import admin
from order_app.models import Order, Contractor
from warehouse_app.admin import CargoInLine


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [CargoInLine]
    list_display = ("__str__", "id",)
