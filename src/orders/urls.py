from django.urls import path
from src.orders.views import (
    add_new_order, delete_active_order,
)


app_name = 'orders'

urlpatterns = [
    path('add-new-order', add_new_order, name='add-new-order'),
    path('delete-active-order', delete_active_order, name='delete-active-order'),
]
