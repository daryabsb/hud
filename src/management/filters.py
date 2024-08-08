import django_filters
from src.pos.models import CashRegister
from src.accounts.models import Customer, User
from src.products.models import Product
import ast
from django.db.models import Q, F, Subquery, OuterRef
from django.views.generic import ListView
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.documents.models import Document, DocumentItem, DocumentType
from src.documents.forms import DocumentFilterForm
from src.core.utils import get_fields, get_columns


class DocumentFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        label='Product',
        method='filter_by_product'
    )
    customer = django_filters.ModelChoiceFilter(
        queryset=Customer.objects.all(),
        label='Customer'
    )
    cash_register = django_filters.ModelChoiceFilter(
        queryset=CashRegister.objects.all(),
        label='Cash Register',
        to_field_name='number'
    )
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='User'
    )
    document_type = django_filters.ModelChoiceFilter(
        queryset=DocumentType.objects.all(),
        label='Document Type'
    )
    reference_document_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='External Document'
    )
    paid_status = django_filters.BooleanFilter(
        label='Paid Status'
    )
    start_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='lte',
        label='End Date'
    )

    class Meta:
        model = Document
        fields = ['customer', 'cash_register', 'user',
                  'document_type', 'paid_status', 'start_date', 'end_date']

    def filter_by_product(self, queryset, name, value):
        document_items_subquery = DocumentItem.objects.filter(
            document=OuterRef('pk'),
            product=value
        ).values('document')
        return queryset.filter(Q(id__in=Subquery(document_items_subquery)))

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)

        # Handle search_value separately
        search_value = self.data.get('search_value', None)
        print('filter data is: ', self.filters)
        if search_value:
            qs = qs.filter(
                Q(name__icontains=search_value)
                | Q(number__icontains=search_value)
                | Q(reference_document_number__icontains=search_value)
                | Q(internal_note__icontains=search_value)
                | Q(stock_date__icontains=search_value)
                | Q(created__icontains=search_value)
                | Q(order__name__icontains=search_value)
                | Q(customer__name__icontains=search_value)
                | Q(cash_register__name__icontains=search_value)
                | Q(warehouse__name__icontains=search_value)
            )

        return qs
