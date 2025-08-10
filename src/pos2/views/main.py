from django.shortcuts import get_object_or_404, render
from src.orders.models import get_orders, PosOrder
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from django.contrib.auth.decorators import login_required
from src.accounts.models import get_customers
from src.configurations.models import get_prop
from src.finances.models.models_payment_type import get_tree_nodes as get_payment_types
from src.configurations.models import get_menus
from src.pos.forms import PosOrderForm
from src.pos2.utils import prepare_order_context
from src.pos2.const import active_order_template


@login_required
def pos_home(request, nunmber=None):
    orders = get_orders(user=request.user)
    context = {'orders': orders, }
    return render(request, 'cotton/pos/home/index.html', context)


@login_required
def pos_order(request, number):
    context = prepare_order_context(request, number)
    if request.htmx:
        return render(request, active_order_template, context)
    return render(request, 'cotton/pos/order/index.html', context)
