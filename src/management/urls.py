
from django.urls import path
from src.management.views import (
    mgt_home, mgt_products, mgt_stocks
)


app_name = 'mgt'

urlpatterns = [
    path('', mgt_home, name='mgt-home'),
    path('products/', mgt_products, name='products'),
    path('stocks/', mgt_stocks, name='stocks'),
]