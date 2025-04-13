
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.products.api.views import ProductViewSet, products_columns_view
from src.products import views


router = DefaultRouter()
router.register('list', ProductViewSet, basename='api-list')


app_name = "products"

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/products-columns/', products_columns_view, name='products-columns'),
    path('search-products-datatable/<str:app_name>/<str:model>/',
         views.product_search_datatable, name='search-products'),
]
