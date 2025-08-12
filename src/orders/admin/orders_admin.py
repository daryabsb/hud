from django.contrib import admin

from src.orders.models import PosOrder


@admin.register(PosOrder)
class PosOrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'customer', 
                    # 'discount', 'discount_sign', 'discounted_amount', 
                    'is_active', 'is_enabled', 'paid_status', 

                    'total','created'
                    )
    ordering = ('-created', )
