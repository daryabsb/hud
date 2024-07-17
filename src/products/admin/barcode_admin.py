from django.contrib import admin

from src.products.models import Barcode

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'value', 'image', 'user_name', 'created')
    ordering = ('created', )
    list_filter = ('product', )

    def product_name(self, obj):
        return obj.product.name

    def user_name(self, obj):
        return obj.user.name