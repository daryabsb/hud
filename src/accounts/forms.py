
from django import forms
from src.accounts.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'code']
        # widgets = {
        #     'name': forms.TextInput(attrs={'id': 'customer_name', 'name': 'customer_name'}),
        #     'email': forms.EmailInput(attrs={'id': 'customer_email', 'name': 'customer_email'}),
        #     'code': forms.TextInput(attrs={'id': 'customer_code', 'name': 'customer_code'}),
        # 'is_customer': forms.BooleanField(attrs={'type': 'hidden'}),
        # 'is_supplier': forms.BooleanField(attrs={'type': 'hiddent'}),
        # }


class CustomerFieldForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False,
        label='Customer',
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm',
                # 'hx-get': '',
                # 'hx-target': '#orderCustomerButton',
                # 'hx-get': '',

            }
        )
    )

    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)
        if customer:
            self.fields['customer'].initial = customer
