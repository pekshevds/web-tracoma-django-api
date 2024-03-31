from django.urls import path
from main_app.views import IndexView

app_name = 'main_app'

urlpatterns = [
    path('', IndexView.as_view(), name='show-index-page'),
]
