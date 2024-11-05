from django import forms
from src.accounts.models import Customer
from src.documents.models import Document
from src.core.utils import generate_number

add_doc_item_htmx = {
    'hx-get': '/mgt/add-document-change-qty/',
    'hx-target': '#add-product-form-render',
    'hx-swap': 'outerHTML',
    'hx-include': '#add-doc-create-item-form',
}


class DocumentForm(forms.ModelForm):
    number = forms.CharField(
        required=False, label='Number',
        initial=generate_number('order'),
        strip=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    customer = forms.ModelChoiceField(
        # queryset=Customer.objects.filter(is_customer=True),
        queryset=Customer.objects.none(),
        required=False, label=None,
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

    class Meta:
        model = Document
        fields = (
            'number',
            'customer',
            'discount_type',
            'discount',
        )
        # fields = '__all__'

    def __init__(self, *args, **kwargs):

        document_type = kwargs.get('document_type', None)
        user = kwargs.get('user', None)

        # if initial:
        #     document_type = initial.get('document_type')
        if document_type:
            print('document_type_name = ', document_type.name)
            print('user_name = ', user.name)
            # print(document_type.name)

            if document_type.category.id == 1:
                print('Purchase')
            elif document_type.category.id == 2:
                print('Sale')
            elif document_type.category.id == 3:
                print('Inventory')
            elif document_type.category.id == 4:
                print('Loss and Damage')

        # print(self._meta.fields[2])


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


'''
from src.orders.forms import DocumentForm
from src.accounts.models import User
from src.documents.models import DocumentType


dt = DocumentType.objects.get(id=3)
user = User.objects.first()

form = DocumentForm(initial={'document_type':dt,'user':user})

print(form['number'].value())

print(form['customer'].value()) 
None
form.save()

document = form.save(commit=False)
document.user = user
document.save()



document.document_type = dt
document.save()

[
    'Meta', 'add_error', 'add_initial_prefix', 'add_prefix', 'as_div', 'as_p', 
    'as_table', 'as_ul', 'base_fields', 'changed_data', 'clean', 'declared_fields', 
    'default_renderer', 'errors', 'field_order', 'full_clean', 'get_context', 
    'get_initial_for_field', 'has_changed', 'has_error', 'hidden_fields', 'is_multipart', 
    'is_valid', 'media', 'non_field_errors', 'order_fields', 'prefix', 'render', 'save', 
    'template_name', 'template_name_div', 'template_name_label', 'template_name_p', 
    'template_name_table', 'template_name_ul', 'use_required_attribute', 'validate_unique', 
    'visible_fields'
    ]
'''
