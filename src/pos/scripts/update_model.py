from random import randrange
from src.stock.models import Stock
from src.accounts.models import User, Warehouse
from src.products.models import Product
from loguru import logger

def run():
    user = User.objects.first()
    warehouse = Warehouse.objects.first()
    products = Product.objects.all()

    for product in products:
        stock = Stock.objects.create(
            user=user,product=product,warehouse=warehouse,quantity=randrange(250)
        )
        logger.success(
            "Stock created for {}:> {}", 
            stock.product.name,stock.quantity, 
            feature="f-strings")