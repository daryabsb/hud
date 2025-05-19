from django.urls import re_path

from src.orders.consumers import (
    OrdersConsumer, OrdersCountConsumer
                                )

websocket_urlpatterns = [
    re_path(r'ws/orders-count/', OrdersCountConsumer.as_asgi()),
    re_path(r'ws/orders/', OrdersConsumer.as_asgi()),
]