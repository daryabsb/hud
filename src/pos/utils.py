from django.db import transaction
from src.orders.models import PosOrder


def activate_order_and_deactivate_others(order_id=None):
    with transaction.atomic():
        if order_id:
            order = PosOrder.objects.select_for_update().get(pk=order_id)
        else:
            order = PosOrder.objects.select_for_update().first()
            if not order:
                # If all orders are already active, just return None
                return None

        order.is_active = True
        order.save(update_fields=['is_active'])

        # Deactivate all other orders of the same user
        PosOrder.objects.filter(user=order.user).exclude(
            pk=order.pk).update(is_active=False)

    return order


# def get_context(active_order):
#     from src.hud.calculations import update_order_totals
#     order, discount, tax_amount, tax_rate = update_order_totals(active_order)
#     return {
#         "active_order": order,
#         "discount": discount,
#         "tax_rate": tax_rate,
#         "tax_amount": tax_amount,
#         "dscnt": tax_amount
#     }
