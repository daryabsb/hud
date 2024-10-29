from django import forms
from src.accounts.models import Customer
from src.core.utils import generate_number

add_doc_item_htmx = {
    'hx-get': '/mgt/add-document-change-qty/',
    'hx-target': '#add-product-form-render',
    'hx-swap': 'outerHTML',
    'hx-include': '#add-doc-create-item-form',
}


class CreateSaleForm(forms.Form):
    number = forms.CharField(
        required=False, label='Number',
        initial=generate_number('order'),
        strip=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_customer=True),
        required=False, label='Customer',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    discount_type = forms.ChoiceField(
        required=False, label='Discount type',
        choices=(
            (0, 'Percent'),
            (1, 'Amount'),
        ),
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm', **add_doc_item_htmx,
                '_': '''
                on change 
                    if my value is 0 set #discount-type-sign.innerText to '%'
                    else set #discount-type-sign.innerText to '$'  end'''
            }
        )
    )

    discount = forms.FloatField(
        required=False, label='Discount',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'hx-trigger': 'keyup changed delay:500ms',
                **add_doc_item_htmx
            }
        )
    )
