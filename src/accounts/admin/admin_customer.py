from django.contrib import admin

# Register your models here.
from src.accounts.models import User, Customer


INITIAL_DATA = [
    {"id": 1, "name": "Good Customer",  "email": "customer@email.com", 'code': 'zzz-2323', "is_supplier": False, "is_customer":True,},
    {"id": 2, "name": "Maad Center",    "email": "maad.cen@email.com", 'code': 'mad-6546', "is_supplier": True,  "is_customer":False,},
    {"id": 3, "name": "Wan Company",    "email": "wan.comp@email.com", 'code': 'zzz-2323', "is_supplier": True,  "is_customer":False,},
    {"id": 4, "name": "Fresh Tomato",   "email": "freshtto@email.com", 'code': 'frt-1280', "is_supplier": True,  "is_customer":False,},
    {"id": 5, "name": "Bayad Company",  "email": "bayad.co@email.com", 'code': 'elc-9024', "is_supplier": True,  "is_customer":False,},
    {"id": 6, "name": "Ashley Home",    "email": "ashley.c@email.com", 'code': 'hme-0032', "is_supplier": True,  "is_customer":False,},
    {"id": 7, "name": "Miniso",         "email": "miniso.c@email.com", 'code': 'acs-9654', "is_supplier": True,  "is_customer":False,},
    {"id": 8, "name": "Dar Tawazoo",    "email": "tawazoo3@email.com", 'code': 'goo-2312', "is_supplier": True,  "is_customer":False,},
    {"id": 9, "name": "My Vapery",      "email": "myvape@myvapery.ae", 'code': 'vap-3333', "is_supplier": True,  "is_customer":False,},
]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'updated')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, cus in enumerate(INITIAL_DATA):
            customer = Customer.objects.get(id=cus['id'])
            if not customer:
                user = User.objects.get(email='root@root.com')
                customer = Customer(**cus)
                customer.user = user
                customer.save(force_insert=True)
            else:
                customer.email = cus['email']
                customer.code = cus['code']
                customer.is_supplier = cus['is_supplier']
                customer.is_customer = cus['is_customer']
                customer.save(force_update=True)
