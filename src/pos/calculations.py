
from src.orders.models import PosOrder, PosOrderItem


def create_order_item(user, order_number, product, quantity=1):
    if order_number:
        order = PosOrder.objects.get(number=order_number)
    return PosOrderItem.objects.create(
        user=user,
        order=order,
        product=product,
        quantity=quantity,
        price=product.price
    )


def update_order_totals(order):
    return order, order.discounted_amount, order.total_tax, 1
