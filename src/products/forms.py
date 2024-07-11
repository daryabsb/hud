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
