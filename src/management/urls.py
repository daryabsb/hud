
from django.urls import path
from src.management.views import (
    mgt_home, mgt_products, mgt_stocks, mgt_users,
    mgt_update_permissions,
)


app_name = 'mgt'

urlpatterns = [
    path('', mgt_home, name='mgt-home'),
    path('products/', mgt_products, name='products'),
    path('stocks/', mgt_stocks, name='stocks'),
    path('users/', mgt_users, name='users'),
    path('update-permissions/', mgt_update_permissions, name='update-permissions'),
]