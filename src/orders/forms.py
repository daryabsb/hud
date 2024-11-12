from django import forms
from src.accounts.models import Customer
from src.documents.models import Document
from src.core.utils import generate_number
from datetime import datetime, timedelta
from django.utils.text import slugify

today = datetime.now()
due_date = today + timedelta(days=15)

add_doc_item_htmx = {
    'hx-get': '/mgt/add-document-change-qty/',
    'hx-target': '#add-product-form-render',
    'hx-swap': 'outerHTML',
    'hx-include': '#add-doc-create-item-form',
}


class CustomDateInput(forms.DateInput):
    template_name = 'mgt/widgets/date-widget.html'

    def __init__(self, attrs=None):
        final_attrs = {'type': 'date', 'class': 'form-control form-control-sm'}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class DocumentForm(forms.ModelForm):
    number = forms.CharField(
        required=False, label='Number',
        # initial=generate_number('order'),
        strip=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_customer=True),
        required=False, label=None,
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )
    reference_document_number = forms.CharField(
        max_length=100, required=False, label='External Document',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    date = forms.DateField(
        initial=today,
        required=False,
        widget=CustomDateInput(),
        label='Date'
    )
    due_date = forms.DateField(
        initial=due_date,
        required=False,
        widget=CustomDateInput(),
        label='Due Date'
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
            'document_type',
            'reference_document_number',
            # 'date',
            # 'due_date',
        )
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get initial document_type if available
        document_type = self.initial.get('document_type', None)

        print('document_type = ', document_type)
        self.fields['number'].initial = generate_number(
            slugify(document_type.name).lower())
        # Adjust customer field based on document_type
        if document_type.category.id == 1:
            self.fields['customer'].queryset = Customer.objects.filter(
                is_customer=True)
        elif document_type.category.id == 2:
            self.fields['customer'].queryset = Customer.objects.filter(
                is_supplier=True)
        else:
            # Hide customer field for other types
            self.fields['customer'].queryset = Customer.objects.all()
            # self.fields['customer'].widget = forms.HiddenInput()


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
