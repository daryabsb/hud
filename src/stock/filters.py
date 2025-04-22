import django_filters
from django.db.models import F, OuterRef, Subquery
from src.stock.models import Stock, StockControl
from src.accounts.models import Warehouse

class StockFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains', label='Product')
    warehouse = django_filters.ModelChoiceFilter(queryset=Warehouse.objects.all())
    quantity__gt = django_filters.NumberFilter(field_name='quantity', lookup_expr='gt', label='Quantity >')
    quantity__lt = django_filters.NumberFilter(field_name='quantity', lookup_expr='lt', label='Quantity <')

    class Meta:
        model = Stock
        fields = ['product_name', 'warehouse', 'quantity__gt', 'quantity__lt']
