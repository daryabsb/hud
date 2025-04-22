import random
from src.stock.const import STOCK_INITIAL_DATA, STOCK_CONTROL_INITIAL_DATA
from django.contrib import admin
from src.stock.models import Stock, StockControl
from src.accounts.models import Warehouse, User, Customer
from src.products.models import Product
# Register your models here.
# random.choice([-40, 40])
# int(round(quantity * 0.75,0)) 

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'product', 'quantity', 'created', 'updated')
    ordering = ('id', )
    list_filter = ('product', 'warehouse', )
    search_fields = ('product__name', 'warehouse__name')
    readonly_fields = ('created', 'updated')

    @staticmethod
    def initial_data():
        for index, stock in enumerate(STOCK_INITIAL_DATA):
            warehouse = Warehouse.objects.get(id=stock['warehouse'])
            product = Product.objects.get(id=stock['product'])

            stock_obj = Stock.objects.filter(
                warehouse=warehouse, 
                product=product
                ).first()
            
            if not stock_obj:
                user = User.objects.get(email='root@root.com')
                stock_obj = Stock(
                    id=stock['id'],user=user, product=product, 
                    warehouse=warehouse, quantity=int(stock['quantity'])
                    )
                stock_obj.save(force_insert=True)
            else:
                stock_obj.quantity = int(stock['quantity'])
                stock_obj.save(force_update=True)


@admin.register(StockControl)
class StockControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'reorder_point', 'is_low_stock_warning_enabled',
                    'low_stock_warning_quantity')
    ordering = ('id', )
    list_filter = ('product', )

    @staticmethod
    def initial_data():
        for index, stock_control in enumerate(STOCK_CONTROL_INITIAL_DATA):
            product = Product.objects.get(id=stock_control['product'])
            customer = Customer.objects.get(id=stock_control['customer'])

            stock_control_obj = StockControl.objects.filter(product=product).first()
            
            if not stock_control_obj:
                user = User.objects.get(email='root@root.com')
                low_stock_warning_quantity=round(stock_control['reorder_point'] * 0.6,1)

                stock_control_obj = StockControl(
                    id=stock_control['id'],user=user, product=product, 
                    customer=customer, reorder_point=stock_control['reorder_point'],
                    preferred_quantity=stock_control['preferred_quantity'],
                    low_stock_warning_quantity=low_stock_warning_quantity
                    )
                stock_control_obj.save(force_insert=True)
            else:
                stock_control_obj.customer=customer
                stock_control_obj.save(force_update=True)