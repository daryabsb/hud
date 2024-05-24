
from src.orders.models import PosOrderItem


def create_order_item(user, order, product, quantity=1):
    return PosOrderItem.objects.create(
        user=user,
        order=order,
        product=product,
        quantity=quantity,
        price=product.price
    )


def update_order_totals(order):
    return order, order.discounted_amount, order.total_tax, 1
