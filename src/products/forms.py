from django import forms
from src.products.models import Product, ProductGroup

class ProductForm(forms.ModelForm):
    # parent_group = forms.ModelChoiceField(
    #     queryset=ProductGroup.objects.all(),
    #     empty_label="Select Product Group",
    #     label="Parent Group",
    #     widget=forms.Select
    # )

    class Meta:
        model = Product
        fields = '__all__'