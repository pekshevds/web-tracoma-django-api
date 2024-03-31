from django.urls import path, include
from rest_framework.authtoken import views


app_name = 'api_app'

urlpatterns = [
    path('users/', include('auth_app.urls', namespace='auth_app')),
    path('warehouse/', include('warehouse_app.urls', namespace='warehouse_app')),
    path('order/', include('order_app.urls', namespace='order_app')),
    path('api-token-auth/', views.obtain_auth_token),
]
