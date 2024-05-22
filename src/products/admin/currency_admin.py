from django.contrib import admin

from src.products.models import Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'code', 'updated')
