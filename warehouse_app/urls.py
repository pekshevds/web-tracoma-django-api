from django.urls import path
from warehouse_app.views import (
    WarehouseView,
    CargoView
)


app_name = "warehouse_app"

urlpatterns = [
    path("warehouses/", WarehouseView.as_view(), name=""),
    path("cargos/", CargoView.as_view(), name=""),
]
