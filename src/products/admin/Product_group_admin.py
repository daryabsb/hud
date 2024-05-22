from django.contrib import admin

from src.products.models import ProductGroup

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    pass