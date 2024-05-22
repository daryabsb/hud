from django.contrib import admin

from src.products.models import Barcode

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    pass