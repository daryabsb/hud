import django_filters
from django import forms
from django.db.models import Q, F, OuterRef, Subquery
from src.stock.models import Stock, StockControl
from src.accounts.models import Warehouse
from src.products.models import ProductGroup


class StockFilter(django_filters.FilterSet):
    categories = django_filters.ModelChoiceFilter(
        queryset=ProductGroup.objects.filter(
            is_enabled=True).select_related('user'),
        label='Categories',
        to_field_name='id',
        initial=ProductGroup.objects.get(id=1).id,
        widget=forms.Select(attrs={
            # 'id': 'search-categories',
            'class': 'form-select form-select-lg',
            'hx-get': '/pos/search/stocks/',
            'hx-trigger': 'change',
            'hx-target': '#search-products-tab',
            # 'hx-include': '#search-stocks-products'
        }),
        method='filter_by_categories',
        empty_label=None,
    )

    product_name = django_filters.CharFilter(
        method='filter_product_name',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg pe-35px first-input',
            # 'id': 'search-stocks-products',
            'placeholder': 'Search products',
            'autocomplete': 'off',
            'hx-get': '/pos/search/stocks/',
            'hx-trigger': 'keyup changed delay:1s',
            'hx-target': '#search-products-tab',
            # 'hx-include': '#search-categories'
        }),
        label='Product')
    warehouse = django_filters.ModelChoiceFilter(
        queryset=Warehouse.objects.all())
    quantity__gt = django_filters.NumberFilter(
        field_name='quantity', lookup_expr='gt', label='Quantity >')
    quantity__lt = django_filters.NumberFilter(
        field_name='quantity', lookup_expr='lt', label='Quantity <')

    class Meta:
        model = Stock
        fields = ['categories', 'product_name',
                  'warehouse', 'quantity__gt', 'quantity__lt']

    def filter_product_name(self, queryset, name, value):
        return queryset.filter(
            Q(product__name__icontains=value) |
            Q(product__parent_group__name__icontains=value)
        )

    def filter_by_categories(self, queryset, name, value):
        return queryset.filter(
            Q(product__parent_group=value) |
            Q(product__parent_group__parent__name=value)
        ).distinct()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.data.get('categories'):
    #         default = ProductGroup.objects.filter(is_enabled=True).first()
    #         if default:
    #             self.form.fields['categories'].initial = default.id
# class StockFilter(django_filters.FilterSet):
#     category = django_filters.CharFilter(
#         method='filter_product_name', label='Product')
#     product_name = django_filters.CharFilter(
#         method='filter_product_name', label='Product')
#     warehouse = django_filters.ModelChoiceFilter(
#         queryset=Warehouse.objects.all())
#     quantity__gt = django_filters.NumberFilter(
#         field_name='quantity', lookup_expr='gt', label='Quantity >')
#     quantity__lt = django_filters.NumberFilter(
#         field_name='quantity', lookup_expr='lt', label='Quantity <')

#     class Meta:
#         model = Stock
#         fields = ['product_name', 'warehouse', 'quantity__gt', 'quantity__lt']
