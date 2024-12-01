from django.contrib import admin

from src.orders.models import PosOrderItem

@admin.register(PosOrderItem)
class PosOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'discount',
                    'discount_type', 'created')
    ordering = ('-created', )
    list_filter = ('created', 'order', )