from django.contrib import admin
from .admin_customer import CustomerAdmin
from .admin_warehouse import WarehouseAdmin
from src.stock.models import Stock
# Register your models here.
from src.accounts.models import User, Company, Store, Logo

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Store)
admin.site.register(Logo)
admin.site.register(Stock)
