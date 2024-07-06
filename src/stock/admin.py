from django.contrib import admin
from src.stock.models import Stock, StockControl
# Register your models here.


@admin.register(StockControl)
class StockControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'reorder_point', 'is_low_stock_warning_enabled',
                    'low_stock_warning_quantity')
    ordering = ('id', )
    list_filter = ('product', )
