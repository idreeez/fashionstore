from django.urls import path
from .views import order_success, create_order

app_name = "orders"

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('success/<int:order_id>/', order_success, name='order_success'),
]
