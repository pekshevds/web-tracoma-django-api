from django.urls import path
from order_app.views import (
    ContractorView,
    OrderView
)

app_name = 'order_app'

urlpatterns = [
    path("contractors/", ContractorView.as_view(), name=""),
    path("orders/", OrderView.as_view(), name=""),
]
