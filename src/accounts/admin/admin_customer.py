from django.contrib import admin

# Register your models here.
from src.accounts.models import User, Customer


INITIAL_DATA = [
    {"id": 1, "name": "Good Customer", "email": 'customer@email.com'},
]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'updated')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, cus in enumerate(INITIAL_DATA):
            customer = Customer.objects.filter(name=cus['name']).first()
            if not customer:
                user = User.objects.get(email='root@root.com')
                customer = Customer(**cus)
                customer.user = user
                customer.save(force_insert=True)
            else:
                customer.email = cus['email']
                customer.save(force_update=True)
