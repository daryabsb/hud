from django import forms

from src.products.models import Product
from src.accounts.models import User, Customer, Warehouse
from src.pos.models import CashRegister
from src.documents.models import DocumentType

from datetime import datetime, timedelta

today = datetime.now()
due_date = today + timedelta(days=15)

SET_ENDDATE_MIN_AND_VALUE = f'''
        on change
            set the min of next <input/> to my value
            set the value of next <input/> to my value
        end
        '''


class DocumentFilterForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False, label='Product',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False, label='Customer',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    cash_register = forms.ModelChoiceField(
        queryset=CashRegister.objects.all(),
        required=False, label='Cash register',
        to_field_name='number',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )

    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        required=False, label='Warehouse',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False, label='User',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        required=False, label='Document type',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    reference_document_number = forms.CharField(
        max_length=100, required=False, label='External document',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    paid_status = forms.TypedChoiceField(
        required=False, label='Paid Status',
        choices=[('', '----'), (True, 'Paid'), (False, 'Unpaid')],
        coerce=lambda x: x == 'True',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    start_date = forms.DateField(
        required=False, widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
                '_': SET_ENDDATE_MIN_AND_VALUE

            }),
        label='Period'
    )
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
                #   '_': 'on change set the max of previous <input/> to my value'
            }),
        label='End Date'
    )


class DocumentCreateForm(forms.Form):
    number = forms.CharField(
        required=False, label='Number',
        initial= '45fd45fd',
        strip=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_customer=False,is_supplier=True),
        required=False, label='Vendor',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    reference_document_number = forms.CharField(
        max_length=100, required=False, label='External document',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    date = forms.DateField(
        initial=today,
        required=False, 
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
                '_': SET_ENDDATE_MIN_AND_VALUE

            }),
        label='Date'
    )
    due_date = forms.DateField(
        initial=due_date,
        required=False, 
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
                #   '_': 'on change set the max of previous <input/> to my value'
            }),
        label='Due Date'
    )
    stock_date = forms.DateField(
        initial=today,
        required=False, 
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
                #   '_': 'on change set the max of previous <input/> to my value'
            }),
        label='Stock Date'
    )
    paid_status = forms.BooleanField(
        required=False, label='Paid Status',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# class AddItemToDocumentForm(forms.Form):
#     product = forms.ModelChoiceField(
#         queryset=Product.objects.filter(is_enabled=True),
#         required=False, label='Product',
#         to_field_name='id',
#         widget=forms.Select(
#             attrs={'class': 'form-select form-select-sm'}
#         )
#     )
#     quantity = forms.IntegerField(
#         required=False, label='Quantity',
#         initial= 1,
#         strip=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control form-control-sm'}
#         )
#     )