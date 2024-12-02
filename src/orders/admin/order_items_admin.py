from django.contrib import admin

from src.orders.models import PosOrderItem


@admin.register(PosOrderItem)
class PosOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product',  'price', 'quantity', 'item_total', 'discounted_amount',
                    'discount_sign', 'created')
    ordering = ('-created', )
    list_filter = ('created', 'order', )
