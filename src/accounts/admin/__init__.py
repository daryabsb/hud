from django.contrib import admin
from .admin_customer import CustomerAdmin
# Register your models here.
from src.accounts.models import User, Company, Store, Logo

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Store)
admin.site.register(Logo)
