from django.contrib import admin

# Register your models here.
from src.accounts.models import User, Customer

admin.site.register(User)
admin.site.register(Customer)
