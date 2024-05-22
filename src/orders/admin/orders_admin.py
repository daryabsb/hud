from django.contrib import admin

from src.orders.models import PosOrder

@admin.register(PosOrder)
class PosOrderAdmin(admin.ModelAdmin):
    pass