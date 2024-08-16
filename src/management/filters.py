from django import forms
from datetime import datetime
from django_filters import (
    FilterSet, CharFilter, ModelChoiceFilter, TypedChoiceFilter, DateFilter,
    BooleanFilter,
)
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


class DocumentFilterForm(FilterSet):
    product = ModelChoiceFilter(
        queryset=Product.objects.all(),
        label='Product',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        method='filter_by_product'
    )
    customer = ModelChoiceFilter(
        queryset=Customer.objects.all(),
        label='Customer',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        method='filter_by_customer'
    )
    cash_register = ModelChoiceFilter(
        queryset=CashRegister.objects.all(),
        label='Cash Register',
        to_field_name='number',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        method='filter_by_cash_register'
    )
    warehouse = ModelChoiceFilter(
        queryset=Warehouse.objects.all(),
        label='Warehouse',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        method='filter_by_warehouse'
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
        method='filter_by_document_type'
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
    start_date = DateFilter(
        label='Period',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
        method='filter_by_start_date'
    )
    end_date = DateFilter(
        label='End Date',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
        method='filter_by_end_date'
    )

    def __init__(self, data=None, queryset=None, *, customer=None, request=None, prefix=None):
        # Preprocess the data to handle non-standard query parameters
        # if request is not None:
        if request is not None:
            customer = request.get('search[value][customer]', None)
        if data is not None:
            print('data = ', data)
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

        print('self_request = ', request)
        super().__init__(data, queryset=queryset, request=request, prefix=prefix)

    class Meta:
        model = Document
        fields = ['customer']

    @property
    def qs(self):
        queryset = super().qs
        # Additional filtering logic can be added here if needed
        return queryset

    def filter_by_product(self, queryset, name, value):
        return queryset.filter(document_items__product=value).distinct()

    def filter_by_customer(self, queryset, name, value):
        print('self.request = ', self.request)
        return queryset.filter(customer=value)

    def filter_by_document_type(self, queryset, name, value):
        return queryset.filter(document_type=value)

    def filter_by_cash_register(self, queryset, name, value):
        return queryset.filter(cash_register=value)

    def filter_by_warehouse(self, queryset, name, value):
        return queryset.filter(warehouse=value)

    def filter_by_paid_status(self, queryset, name, value):
        return queryset.filter(paid_status=value)

    def filter_by_start_date(self, queryset, name, value):
        if value:
            start_date = make_aware(datetime.strptime(
                f"{value} 00:00:00", '%Y-%m-%d %H:%M:%S'))
            return queryset.filter(created__gte=start_date)
        return queryset

    def filter_by_end_date(self, queryset, name, value):
        if value:
            end_date = make_aware(datetime.strptime(
                f"{value} 23:59:59", '%Y-%m-%d %H:%M:%S'))
        else:
            end_date = now()
        return queryset.filter(created__lte=end_date)


class DocumentFilterOld(FilterSet):
    product = ModelChoiceFilter(
        queryset=Product.objects.all(),
        label='Product',
        method='filter_by_product'
    )
    customer = ModelChoiceFilter(
        queryset=Customer.objects.all(),
        label='Customer'
    )
    cash_register = ModelChoiceFilter(
        queryset=CashRegister.objects.all(),
        label='Cash Register',
        to_field_name='number'
    )
    user = ModelChoiceFilter(
        queryset=User.objects.all(),
        label='User'
    )
    document_type = ModelChoiceFilter(
        queryset=DocumentType.objects.all(),
        label='Document Type'
    )
    reference_document_number = CharFilter(
        lookup_expr='icontains',
        label='External Document'
    )
    paid_status = BooleanFilter(
        label='Paid Status'
    )
    start_date = DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Start Date'
    )
    end_date = DateFilter(
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


data = {
    'datatables': '1',
    'draw': '2',
    'columns[0][data]': 'id', 'columns[0][name]': 'id', 'columns[0][searchable]': 'false', 'columns[0][orderable]': 'false', 'columns[0][search][value]': '',
    'columns[0][search][regex]': 'false',

    'columns[1][data]': 'number', 'columns[1][name]': 'number', 'columns[1][searchable]': 'true', 'columns[1][orderable]': 'false',
    'columns[1][search][value]': '', 'columns[1][search][regex]': 'false',

    'columns[2][data]': 'customer__name', 'columns[2][name]': 'customer', 'columns[2][searchable]': 'true', 'columns[2][orderable]': 'false',
    'columns[2][search][value]': '1', 'columns[2][search][regex]': 'false',

    'columns[3][data]': 'cash_register__name', 'columns[3][name]': 'cash_register', 'columns[3][searchable]': 'true', 'columns[3][orderable]': 'false',
    'columns[3][search][value]': '', 'columns[3][search][regex]': 'false',

    'columns[4][data]': 'document_type__name', 'columns[4][name]': 'document_type', 'columns[4][searchable]': 'true', 'columns[4][orderable]': 'false',
    'columns[4][search][value]': '', 'columns[4][search][regex]': 'false',

    'columns[5][data]': 'warehouse__name', 'columns[5][name]': 'warehouse', 'columns[5][searchable]': 'true', 'columns[5][orderable]': 'false',
    'columns[5][search][value]': '', 'columns[5][search][regex]': 'false',

    'columns[6][data]': 'date', 'columns[6][name]': 'date', 'columns[6][searchable]': 'false', 'columns[6][orderable]': 'false', 'columns[6][search][value]': '',
    'columns[6][search][regex]': 'false',

    'columns[7][data]': 'user__name', 'columns[7][name]': 'user', 'columns[7][searchable]': 'false', 'columns[7][orderable]': 'false',
    'columns[7][search][value]': '', 'columns[7][search][regex]': 'false',

    'columns[8][data]': 'reference_document_number', 'columns[8][name]': 'reference_document_number', 'columns[8][searchable]': 'false',
    'columns[8][orderable]': 'false', 'columns[8][search][value]': '', 'columns[8][search][regex]': 'false',

    'columns[9][data]': 'internal_note', 'columns[9][name]': 'internal_note', 'columns[9][searchable]': 'false', 'columns[9][orderable]': 'false',
    'columns[9][search][value]': '', 'columns[9][search][regex]': 'false',

    'columns[10][data]': 'note', 'columns[10][name]': 'note', 'columns[10][searchable]': 'false', 'columns[10][orderable]': 'false',
    'columns[10][search][value]': '', 'columns[10][search][regex]': 'false',
    'columns[11][data]': 'due_date', 'columns[11][name]': 'due_date', 'columns[11][searchable]': 'false', 'columns[11][orderable]': 'false',
    'columns[11][search][value]': '', 'columns[11][search][regex]': 'false',

    'columns[12][data]': 'discount', 'columns[12][name]': 'discount', 'columns[12][searchable]': 'false', 'columns[12][orderable]': 'false',
    'columns[12][search][value]': '', 'columns[12][search][regex]': 'false',

    'columns[13][data]': 'discount_type', 'columns[13][name]': 'discount_type', 'columns[13][searchable]': 'false', 'columns[13][orderable]': 'false',
    'columns[13][search][value]': '', 'columns[13][search][regex]': 'false', 'columns[14][data]': 'discount_apply_rule', 'columns[14][name]':
    'discount_apply_rule', 'columns[14][searchable]': 'false', 'columns[14][orderable]': 'false', 'columns[14][search][value]': '',
    'columns[14][search][regex]': 'false', 'columns[15][data]': 'paid_status', 'columns[15][name]': 'paid_status', 'columns[15][searchable]': 'true',
    'columns[15][orderable]': 'false', 'columns[15][search][value]': '', 'columns[15][search][regex]': 'false', 'columns[16][data]': 'stock_date',
    'columns[16][name]': 'stock_date', 'columns[16][searchable]': 'false', 'columns[16][orderable]': 'false', 'columns[16][search][value]': '',
    'columns[16][search][regex]': 'false', 'columns[17][data]': 'total', 'columns[17][name]': 'total', 'columns[17][searchable]': 'false',
    'columns[17][orderable]': 'false', 'columns[17][search][value]': '', 'columns[17][search][regex]': 'false', 'columns[18][data]': 'is_clocked_out',
    'columns[18][name]': 'is_clocked_out', 'columns[18][searchable]': 'false', 'columns[18][orderable]': 'false', 'columns[18][search][value]': '',
    'columns[18][search][regex]': 'false', 'columns[19][data]': 'created', 'columns[19][name]': 'created', 'columns[19][searchable]': 'true',
    'columns[19][orderable]': 'false', 'columns[19][search][value]': '', 'columns[19][search][regex]': 'false', 'columns[20][data]': 'updated',
    'columns[20][name]': 'updated', 'columns[20][searchable]': 'true', 'columns[20][orderable]': 'false', 'columns[20][search][value]': '',
    'columns[20][search][regex]': 'false', 'columns[21][data]': 'product', 'columns[21][name]': '', 'columns[21][searchable]': 'true',
    'columns[21][orderable]': 'false', 'columns[21][search][value]': '', 'columns[21][search][regex]': 'false',

    'start': '0', 'length': '5', 'search[value]': '', 'search[regex]': 'false',

    '_': '1723836453125'
}
