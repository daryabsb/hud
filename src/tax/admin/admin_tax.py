from django.contrib import admin
from src.tax.models import Tax, ProductTax
from src.accounts.models import User

INITIAL_DATA = [
    {"id": 1, "name": "VAT", "rate": 5.0, "is_tax_on_total": True}
]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rate',
                    'is_tax_on_total', 'amount', 'created')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, tx in enumerate(INITIAL_DATA):
            tax = Tax.objects.filter(name=tx['name']).first()
            if not tax:
                user = User.objects.filter(is_superuser=True).first()
                tax = Tax(user=user, **tx)
                tax.save(force_insert=True)
            else:
                tax.id = tx['id']
                tax.is_tax_on_total = tx["is_tax_on_total"]
                tax.save(force_update=True)
