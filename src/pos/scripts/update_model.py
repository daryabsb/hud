from src.hud.models import Tax, PosOrder
from loguru import logger

def run():
    active_order = PosOrder.objects.first()
    logger.success(
        "Active order total_tax 1:> {} ", 
        active_order.total_tax, 
        feature="f-strings")

    tax = Tax.objects.first()
    tax.rate = 2.000
    tax.amount = 0.000
    tax.save()
    
    logger.success(
        "Active order total_tax 2:> {} ", 
        active_order.total_tax, 
        feature="f-strings")