
from django import forms
from src.printers.models import PrintStation, ProductPrintStation


class PrintStationForm(forms.ModelForm):
    class Meta:
        model = PrintStation
        fields = ['name']


class ProductPrintStationForm(forms.ModelForm):
    class Meta:
        model = ProductPrintStation
        fields = ['print_station']
