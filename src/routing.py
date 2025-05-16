from django.urls import re_path

from src.orders.consumers import OrdersConsumer

websocket_urlpatterns = [
    re_path(r'ws/orders/', OrdersConsumer.as_asgi()),
]