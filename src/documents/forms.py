from django import forms

from src.products.models import Product
from src.accounts.models import User, Customer
from src.pos.models import CashRegister
from src.documents.models import DocumentType
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


def get_product_names():
    return Product.objects.values('id', 'name')


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
            attrs={'class': 'form-select form-select-sm mb-3'}
        )
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False, label='Customer',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm mb-3'}
        )
    )
    cash_register = forms.ModelChoiceField(
        queryset=CashRegister.objects.all(),
        required=False, label='Cash register',
        to_field_name='number',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm mb-3'}
        )
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False, label='User',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm mb-3'}
        )
    )
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        required=False, label='Document type',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm mb-3'}
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
        widget=forms.Select(attrs={'class': 'form-select form-select-sm mb-3'})
    )
    date_range = forms.DateTimeField(
        widget=DateTimePickerInput()
    )
    start_date = forms.DateField(
        required=False, widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm mb-3',
                '_': SET_ENDDATE_MIN_AND_VALUE

            }),
        label='Period'
    )
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm mb-3',
                #   '_': 'on change set the max of previous <input/> to my value'
            }),
        label='End Date'
    )
