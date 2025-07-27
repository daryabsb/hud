from django.utils.html import format_html
from django import forms
from src.orders.models import PosOrder
from src.pos2.const import POS_FORM_FIELDS


class PosOrderForm(forms.ModelForm):
    class Meta:
        model = PosOrder
        fields = POS_FORM_FIELDS
        widgets = {
            # need hidden input to post id from customer
            'customer':         forms.HiddenInput(),
            'internal_note':    forms.Textarea(
                attrs={
                    'class': 'form-control first-input',
                    'rows': 3, 'id': 'order-internal-note-id'
                }),  # note are with real form field
            'note':             forms.Textarea(
                attrs={
                    'class': 'form-control first-input',
                    'rows': 3, 'id': 'order-comment-id'
                }),  # ===
            'discount':         forms.NumberInput(),
            'discount_type':    forms.HiddenInput({'id': 'order-discount_type-id'}),
            'paid_status':      forms.RadioSelect(),
            'status':           forms.RadioSelect(),
        }


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
