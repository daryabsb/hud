from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from src.orders.models import PosOrderItem
from src.stock.models import Stock
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

def update_order_subtotal(order):
    subtotal = PosOrderItem.objects.filter(order=order).aggregate(
        total=Sum('item_total')
    )['total'] or 0
    order.item_subtotal = subtotal
    order.save(update_fields=['item_subtotal'])

@receiver(post_save, sender=PosOrderItem)
def decrease_stock_quantity(sender, instance, created, **kwargs):
    if created:
        stock = Stock.objects.filter(product=instance.product, warehouse=instance.order.warehouse).first()
        if stock:
            stock.quantity -= instance.quantity
            stock.save()
    update_order_subtotal(instance.order)


@receiver(post_delete, sender=PosOrderItem)
def restore_stock_quantity(sender, instance, **kwargs):
    stock = Stock.objects.filter(product=instance.product, warehouse=instance.order.warehouse).first()
    if stock:
        stock.quantity += instance.quantity
        stock.save()
    update_order_subtotal(instance.order)