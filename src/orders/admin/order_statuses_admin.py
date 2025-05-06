from django.contrib import admin
from src.accounts.models import User
from src.orders.models import PosOrderStatus

INITIAL_DATA = [
    {'id': 1, 'ordinal': 1, 'name': 'Created', 'color_class': 'warning'},
    {'id': 2, 'ordinal': 2, 'name': 'Rready for pickup', 'color_class': 'info'},
    {'id': 3, 'ordinal': 3, 'name': 'Rready for delivery', 'color_class': 'info'},
    {'id': 4, 'ordinal': 4, 'name': 'To be paid later', 'color_class': 'primary'},
    {'id': 5, 'ordinal': 5, 'name': 'Paid', 'color_class': 'success'},
    {'id': 6, 'ordinal': 6, 'name': 'Cancelled', 'color_class': 'danger'},
    {'id': 7, 'ordinal': 7, 'name': 'Order fulfilled', 'color_class': 'default'},
]

@admin.register(PosOrderStatus)
class PosOrderStatusAdmin(admin.ModelAdmin):
    list_display = ('ordinal', 'name', 'color')
    ordering = ('-ordinal', )
    
    def color(self, obj):
        return obj.color_class
    

    @staticmethod
    def initial_data():
        for index, status in enumerate(INITIAL_DATA):
            user = User.objects.first()
            sts = PosOrderStatus.objects.filter(name=status['name']).first()
            if not sts:
                sts = PosOrderStatus(**status)
                sts.user = user
                sts.save(force_insert=True)
            else:
                sts.name = status['name']
                sts.save(force_update=True)
        
