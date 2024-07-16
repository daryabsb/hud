from django import forms
from src.products.models import (
    Product, ProductGroup, Barcode, ProductComment
)


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class ProductGroupForm(forms.ModelForm):

    class Meta:
        model = ProductGroup
        fields = ('parent', 'name')


class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'code', 'measurement_unit', 'currency', 'image', 'color', 'color2', 'is_enabled',
            'age_restriction', 'is_service', 'is_using_default_quantity', 'parent_group',
            'cost', 'margin', 'price', 'is_tax_inclusive_price', 'is_price_change_allowed',
        ]


class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode
        fields = ['value']


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['comment']


class PriceTagForm(forms.Form):
    # Assuming product is identified by its ID
    product_id = forms.IntegerField(
        widget=forms.HiddenInput())
    margin = forms.CharField(
        max_length=10, initial='10px', label='margin'
    )
    show_name = forms.BooleanField(initial=True, required=False)
    show_price = forms.BooleanField(initial=True, required=False)
    show_sku = forms.BooleanField(initial=True, required=False)
    show_barcode = forms.BooleanField(initial=True, required=False)
    name_color = forms.CharField(max_length=20, initial='black')
    price_color = forms.CharField(max_length=20, initial='red')
    sku_color = forms.CharField(max_length=20, initial='blue')
    price_size = forms.IntegerField(initial=24)
    sku_size = forms.IntegerField(initial=14)
    barcode_height = forms.IntegerField(initial=50)
