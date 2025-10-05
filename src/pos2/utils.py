from src.orders.models import PosOrder, get_orders
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from src.accounts.models import get_customers
from src.finances.models.models_payment_type import get_tree_nodes as get_payment_types
from src.configurations.models import get_menus
from src.pos.forms import PosOrderForm
from django.shortcuts import get_object_or_404


def prepare_order_context(request, order_number=None, item=None):
    """
    Prepares a standard context dictionary for order-related views in pos2 app.

    This utility function centralizes the common context preparation logic used across
    different views in the pos2 app, reducing code duplication.

    Args:
        request: The HTTP request object
        order_number: Optional order number to get a specific order
        item: Optional order item to include in the context

    Returns:
        A dictionary containing the standard context for order-related views
    """
    # Get the active order
    active_order = get_active_order(user=request.user)
    if not active_order or order_number != active_order['number']:
        active_order = aod(request.user, order_number=order_number)
    # Get the order instance if we have an active order
    order_instance = None
    if active_order and active_order.get('number'):
        order_instance = get_object_or_404(
            PosOrder, number=active_order['number'])
    elif order_number:
        order_instance = get_object_or_404(PosOrder, number=order_number)

    # Prepare the context dictionary
    context = {
        'orders': get_orders(user=request.user),
        'menus': get_menus(),
        'payment_types': get_payment_types(),
        'payment_type': get_payment_types()[0],
        'customers': get_customers(user=request.user),
        'active_order': active_order,
        'order': active_order,
    }

    # Add the order form if we have an order instance
    if order_instance:
        context['form'] = PosOrderForm(instance=order_instance)

    # Add the item if provided
    if item:
        context['item'] = item

    return context
