from django.contrib import admin

from src.products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass