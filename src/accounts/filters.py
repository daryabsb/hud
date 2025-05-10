import django_filters
from django import forms
from django.urls import reverse

class CustomersFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg pe-35px first-input',
            # 'id': 'search-stocks-products',
            'placeholder': 'Search Customers',
            'autocomplete': 'off',
            'hx-get': "/pos/search/customers/",
            'hx-trigger': 'keyup changed delay:1s',
            'hx-target': '#search-customers-tab',
            # 'hx-include': '#search-categories'
        }),
        label='Name')

    # name = django_filters.CharFilter(
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control form-control-lg pe-35px first-input',
    #         # 'id': 'search-stocks-products',
    #         'placeholder': 'Search Customers',
    #         'autocomplete': 'off',
    #         'hx-get': "pos/search/customers/",
    #         'hx-trigger': 'keyup changed delay:1s',
    #         'hx-target': '#search-customers-tab',
    #         # 'hx-include': '#search-categories'
    #     }),
    #     label='Name')
