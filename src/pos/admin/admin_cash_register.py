
from django.contrib import admin
from src.pos.models import CashRegister
from src.pos.utils import get_computer_info


@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'created')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        computer_name, computer_number = get_computer_info()
        register = CashRegister.objects.filter(number=computer_number).first()

        if not register:
            register = CashRegister.objects.create()
