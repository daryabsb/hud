
from django import forms
from src.stock.models import StockControl

class StockControlForm(forms.ModelForm):
    class Meta:
        model = StockControl
        fields = ['customer', 'reorder_point', 'preferred_quantity', 'is_low_stock_warning_enabled', 'low_stock_warning_quantity']
