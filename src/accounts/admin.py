from django.contrib import admin

# Register your models here.
from src.accounts.models import User, Customer, Company, Store, Logo

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Store)
admin.site.register(Logo)
