from django import forms
from src.tax.models import ProductTax


class ProductTaxForm(forms.ModelForm):
    class Meta:
        model = ProductTax
        fields = ['tax']