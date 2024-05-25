from django.contrib import admin

# Register your models here.
from src.accounts.models import User, Warehouse


INITIAL_DATA = [
    {"id": 1, "name": "My Warehouse"},
]


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'updated')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, wows in enumerate(INITIAL_DATA):
            warehouse = Warehouse.objects.filter(name=wows['name']).first()
            if not warehouse:
                user = User.objects.get(email='root@root.com')
                warehouse = Warehouse(**wows)
                warehouse.user = user
                warehouse.save(force_insert=True)
            else:
                warehouse.name = wows['name']
                warehouse.save(force_update=True)
