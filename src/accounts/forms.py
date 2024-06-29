
from django import forms
from src.accounts.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'code']