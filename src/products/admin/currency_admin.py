from django.contrib import admin
from src.accounts.models import User
from src.products.models import Currency


INITIAL_DATA = [
    {"id": 1, "name": "IQD", "code": 'IQD'},
    {"id": 2, "name": "USD", "code": 'USD'},
]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'code', 'updated')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, cur in enumerate(INITIAL_DATA):
            currency = Currency.objects.filter(name=cur['name']).first()
            if not currency:
                user = User.objects.get(email='root@root.com')
                currency = Currency(**cur)
                currency.user = user
                currency.save(force_insert=True)
            else:
                currency.code = cur['code']
                currency.save(force_update=True)
