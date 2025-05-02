from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from src.orders.models import PosOrderItem
from src.stock.models import Stock

@receiver(post_save, sender=PosOrderItem)
def decrease_stock_quantity(sender, instance, created, **kwargs):
    if created:
        stock = Stock.objects.filter(product=instance.product, warehouse=instance.order.warehouse).first()
        if stock:
            stock.quantity -= instance.quantity
            stock.save()

@receiver(post_delete, sender=PosOrderItem)
def restore_stock_quantity(sender, instance, **kwargs):
    stock = Stock.objects.filter(product=instance.product, warehouse=instance.order.warehouse).first()
    if stock:
        stock.quantity += instance.quantity
        stock.save()