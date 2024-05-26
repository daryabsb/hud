from django.db import transaction
from src.orders.models import PosOrder
from src.accounts.models import Customer


def get_active_order(active_order=None):
    if not active_order:
        active_order = PosOrder.objects.filter(is_active=True).first()
    active_order.update_items_subtotal()
    active_order.refresh_from_db()
    # logger.success("Active order item_subtotal:> {} ", active_order.item_subtotal, feature="f-strings")
    # logger.success("Active order total:> {} ", active_order.total, feature="f-strings")
    return active_order


def activate_order_and_deactivate_others(user, order_id=None):
    if order_id:
        order = PosOrder.objects.get(pk=order_id)
        order.is_active = True
        order.save(update_fields=['is_active'])

        PosOrder.objects.filter(user=order.user).exclude(
            pk=order.pk).update(is_active=False)

    elif PosOrder.objects.all().count() == 0:
        customer = Customer.objects.first()
        order = PosOrder.objects.create(
            user=user, customer=customer, is_active=True)
    else:
        order = PosOrder.objects.filter(user=user).first()
        # If all orders are already active, just return None
    return order


def get_context(active_order):
    from src.pos.calculations import update_order_totals
    order, discount, tax_amount, tax_rate = update_order_totals(active_order)
    return {
        "active_order": order,
        "discount": discount,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "dscnt": tax_amount
    }
