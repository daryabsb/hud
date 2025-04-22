from django.urls import path
from src.stock.views import stock_list_view

app_name = "stock"

urlpatterns = [
    path("list/", stock_list_view, name="stock-list"),
]