from django.contrib import admin
from src.finances.models import Payment


# @admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

# Register your models here.
