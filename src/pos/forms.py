from django import forms
from src.orders.models import PosOrder

class FixedTaxesForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['fixed_taxes']
        widgets = {
            'fixed_taxes': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.001}),
        }

class TotalTaxRateForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['total_tax_rate']
        widgets = {
            'total_tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.001}),
        }

class PaidStatusForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['paid_status']
        widgets = {
            'paid_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReferenceDocumentNumberForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['reference_document_number']
        widgets = {
            'reference_document_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InternalNoteForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['internal_note']
        widgets = {
            'internal_note': forms.Textarea(attrs={'class': 'form-control'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }

# class DueDateForm(forms.ModelForm):
#     class Meta:
#         model = PosOrder
#         fields = ['due_date']
#         widgets = {
#             'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#         }

from django import forms
from django.utils.html import format_html

class StyledRadioSelect(forms.RadioSelect):
    option_template_name = 'widgets/order-status.html'

class StatusForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label_from_instance = lambda obj: obj.name

# forms.py
class DiscountAndTypeForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = ['discount', 'discount_type']
        widgets = {
            'discount': forms.NumberInput(attrs={'step': 0.01, 'class': 'form-control'}),
            'discount_type': forms.NumberInput(attrs={'step': 0.01, 'class': 'form-control'}),
        }
