from django import forms

from src.products.models import Product
from src.accounts.models import User, Customer, Warehouse
from src.pos.models import CashRegister
from src.documents.models import DocumentType

from datetime import datetime, timedelta

from src.tax.models import Tax

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


# form = DocumentCreateForm(
#           stock_direction=document_type.stock_direction,
#           product=selected_product
#           )


class DocumentCreateForm(forms.Form):
    number = forms.CharField(
        required=False, label='Number',
        initial='45fd45fd',
        strip=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.none(),
        required=False, label='',
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
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
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
            }),
        label='Stock Date'
    )
    paid_status = forms.BooleanField(
        required=False, label='Paid Status',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # You can add price and cost fields here if needed, initialized conditionally

    def __init__(self, *args, **kwargs):
        stock_direction = kwargs.pop('stock_direction', None)
        # Assume product is passed to set price and cost
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        # Adjust queryset and initial values based on stock_direction
        if stock_direction == 2:  # Sale
            self.fields['customer'].queryset = Customer.objects.filter(
                is_customer=True)
            self.fields['customer'].label = 'Customer'
            # if product:
            #     self.fields['price'].initial = product.price
            #     self.fields['cost'].initial = product.cost
        elif stock_direction == 1:  # Purchase
            self.fields['customer'].queryset = Customer.objects.filter(
                is_supplier=True)
            self.fields['customer'].label = 'Vendor'
        elif stock_direction == 0:  # Proforma
            # General query
            self.fields['customer'].queryset = Customer.objects.all()

        # Adjust form field labels or other logic if needed


class AddDocumentItem(forms.Form):
    product = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.none(),
        required=False, label='Customer/Vendor',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )

    quantity = forms.IntegerField(
        required=False, label='Quantity',
        initial=1,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )

    price_before_tax = forms.FloatField(
        required=False, label='Price before tax',
        initial=0.0,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )

    tax = forms.ModelChoiceField(
        queryset=Tax.objects.filter(is_tax_on_total=False),
        required=False, label='Tax',
        to_field_name='id',
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )

    price = forms.FloatField(
        required=False, label='Price',
        initial=0.0,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
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
                'class': 'form-select form-select-sm',
                '_': '''
                on change 
                    if my value is 0 set #discount-type-sign.innerText to '%'
                    else set #discount-type-sign.innerText to '$'  end'''
            }
        )
    )

    discount = forms.FloatField(
        required=False, label='Discount',
        initial=0.0,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )

    total_before_tax = forms.FloatField(
        required=False, label='Total before tax',
        initial=0.0,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )

    total = forms.FloatField(
        required=False, label='Total',
        initial=0.0,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )

    def __init__(self, *args, **kwargs):
        stock_direction = kwargs.pop('stock_direction', None)
        # Assume product is passed to set price and cost
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        # Adjust queryset and initial values based on stock_direction
        if stock_direction == 2:  # Sale
            self.fields['customer'].queryset = Customer.objects.filter(
                is_customer=True)
            self.fields['customer'].initial = Customer.objects.filter(
                is_customer=True).first()
            self.fields['customer'].label = 'Customer'
            if product:
                self.fields['product'].initial = product.id
                self.fields['price'].initial = product.price
                # self.fields['product_cost'].initial = product.cost

        elif stock_direction == 1:  # Purchase
            self.fields['customer'].queryset = Customer.objects.filter(
                is_supplier=True)
            self.fields['customer'].label = 'Vendor'
            self.fields['customer'].initial = Customer.objects.filter(
                is_supplier=True).first()
            if product:
                self.fields['product'].initial = product.id

        elif stock_direction == 0:  # Proforma
            # General query
            self.fields['customer'].queryset = Customer.objects.all()
            self.fields['customer'].initial = Customer.objects.first()


# class DocumentCreateForm2(forms.Form):
#     number = forms.CharField(
#         required=False, label='Number',
#         initial='45fd45fd',
#         strip=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control form-control-sm'}
#         )
#     )
#     customer = forms.ModelChoiceField(
#         queryset=Customer.objects.filter(is_customer=False, is_supplier=True),
#         required=False, label='Vendor',
#         to_field_name='id',
#         widget=forms.Select(
#             attrs={'class': 'form-select form-select-sm'}
#         )
#     )
#     reference_document_number = forms.CharField(
#         max_length=100, required=False, label='External document',
#         widget=forms.TextInput(
#             attrs={'class': 'form-control form-control-sm'}
#         )
#     )
#     date = forms.DateField(
#         initial=today,
#         required=False,
#         widget=forms.DateInput(
#             attrs={
#                 'type': 'date',
#                 'class': 'form-control form-control-sm',
#                 '_': SET_ENDDATE_MIN_AND_VALUE

#             }),
#         label='Date'
#     )
#     due_date = forms.DateField(
#         initial=due_date,
#         required=False,
#         widget=forms.DateInput(
#             attrs={
#                 'type': 'date',
#                 'class': 'form-control form-control-sm',
#                 #   '_': 'on change set the max of previous <input/> to my value'
#             }),
#         label='Due Date'
#     )
#     stock_date = forms.DateField(
#         initial=today,
#         required=False,
#         widget=forms.DateInput(
#             attrs={
#                 'type': 'date',
#                 'class': 'form-control form-control-sm',
#                 #   '_': 'on change set the max of previous <input/> to my value'
#             }),
#         label='Stock Date'
#     )
#     paid_status = forms.BooleanField(
#         required=False, label='Paid Status',
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
#     )


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
