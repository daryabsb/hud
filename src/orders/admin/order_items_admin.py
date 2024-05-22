from django.contrib import admin

from src.orders.models import PosOrderItem

@admin.register(PosOrderItem)
class PosOrderItemAdmin(admin.ModelAdmin):
    pass