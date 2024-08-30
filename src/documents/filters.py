from django import forms
from datetime import datetime
from django_filters import (
    FilterSet, CharFilter, ModelChoiceFilter, TypedChoiceFilter, DateFilter,
    BooleanFilter, RangeFilter, DateFromToRangeFilter
)
from django_filters.widgets import RangeWidget, DateRangeWidget
from src.pos.models import CashRegister
from src.products.models import Product
from django.db.models import Q, F, Subquery, OuterRef

from src.accounts.models import Customer, User, Warehouse
from src.documents.models import Document, DocumentItem, DocumentType
from src.products.models import Product
from src.accounts.models import Customer
from src.pos.models import CashRegister
from src.documents.models import DocumentType, Document

from django.utils.timezone import now, make_aware

from src.core.utils import get_fields

# from django_filters import filters
from django_filters import rest_framework as filters
from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend
from rest_framework_datatables.django_filters.filterset import DatatablesFilterSet
from rest_framework_datatables.django_filters.filters import GlobalFilter


class GlobalChoiceFilter(GlobalFilter, filters.ChoiceFilter):
    pass


class DocumentFilter(FilterSet):
    product = ModelChoiceFilter(
        queryset=Product.objects.all(),
        label='Product',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        method='filter_by_product'
    )
    customer = ModelChoiceFilter(
        field_name='customer',
        queryset=Customer.objects.all(),
        label='Customer2',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        method='filter_by_customer',
    )
    cash_register = ModelChoiceFilter(
        queryset=CashRegister.objects.all(),
        label='Cash Register',
        to_field_name='number',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        # method='filter_by_cash_register'
    )
    warehouse = ModelChoiceFilter(
        queryset=Warehouse.objects.all(),
        label='Warehouse',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        # method='filter_by_warehouse'
    )
    user = ModelChoiceFilter(
        queryset=User.objects.all(),
        label='User',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    document_type = ModelChoiceFilter(
        queryset=DocumentType.objects.all(),
        label='Document Type',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        # method='filter_by_document_type'
    )
    reference_document_number = CharFilter(
        max_length=100, label='External Document',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}),
        lookup_expr='icontains'
    )
    paid_status = TypedChoiceFilter(
        label='Paid Status',
        choices=[('', '----'), (True, 'Paid'), (False, 'Unpaid')],
        coerce=lambda x: x == 'True',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        # method='filter_by_paid_status'
    )
    created = DateFromToRangeFilter(widget=DateRangeWidget(
        # label='Created',
        attrs={
            'placeholder': 'YYYY/MM/DD',
            'class': 'form-control form-control-sm',
            'type': 'date'
        }))

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        # Preprocess the data to handle non-standard query parameters
        # if request is not None:
        print("The data is called: ", data)
        if data is not None:
            customer_id = data.get('search[value][customer]', None)
            if customer_id:
                customer = Customer.objects.get(id=int(customer_id))
                self.filter_by_customer(queryset, value=customer)
        if data is not None:
            customer_id = data.get('search[value][customer]', None)
            if customer_id:
                print('customer_id = ', customer_id)
            # print('data = ', data)
            processed_data = {}
            for key, value in data.items():
                if key.startswith("search[value][") and key.endswith("]"):
                    # Extract the field name, e.g., "product" from "search[value][product]"
                    field_name = key[len("search[value]["):-1]
                    processed_data[field_name] = value
                else:
                    processed_data[key] = value
            data = processed_data
            # print('data = ', data)

        # print('self_request = ', request)
        super().__init__(data, queryset=queryset, request=request, prefix=prefix)

    class Meta:
        model = Document
        fields = [*get_fields('documents')]

    def filter_by_product(self, queryset, name, value):
        return queryset.filter(document_items__product=value).distinct()

    def filter_by_customer(self, queryset, value):
        print('called___________________')
        if value:
            print('selected_product = ', value)
        print('self.request = ', self.request)
        return self.filter_queryset(customer=value)

    # def filter_by_document_type(self, queryset, name, value):
    #     return queryset.filter(document_type=value)

    # def filter_by_cash_register(self, queryset, name, value):
    #     return queryset.filter(cash_register=value)

    # def filter_by_warehouse(self, queryset, name, value):
    #     return queryset.filter(warehouse=value)

    # def filter_by_paid_status(self, queryset, name, value):
    #     return queryset.filter(paid_status=value)

    # def filter_by_start_date(self, queryset, name, value):
    #     if value:
    #         start_date = make_aware(datetime.strptime(
    #             f"{value} 00:00:00", '%Y-%m-%d %H:%M:%S'))
    #         return queryset.filter(created__gte=start_date)
    #     return queryset

    # def filter_by_end_date(self, queryset, name, value):
    #     if value:
    #         end_date = make_aware(datetime.strptime(
    #             f"{value} 23:59:59", '%Y-%m-%d %H:%M:%S'))
    #     else:
    #         end_date = now()
    #     return queryset.filter(created__lte=end_date)
