from django import forms
from src.tax.models import ProductTax, Tax


class ProductTaxForm(forms.ModelForm):
    class Meta:
        model = ProductTax
        fields = ['tax']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tax'].queryset = Tax.objects.filter(is_tax_on_total=False)
