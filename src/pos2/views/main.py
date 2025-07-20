from django.shortcuts import render
from src.orders.models import get_orders  # , PosOrder
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from django.contrib.auth.decorators import login_required
from src.configurations.models import get_menus


@login_required
def pos_home(request, nunmber=None):
    orders = get_orders(user=request.user)
    context = {'orders': orders, }
    return render(request, 'cotton/pos/home/index.html', context)


@login_required
def pos_order(request, number):
    orders = get_orders(user=request.user)
    active_order = aod(request.user, order_number=number)

    context = {
        'orders': orders,
        'menus': get_menus(),
        'active_order': active_order,
    }
    return render(request, 'cotton/pos/order/index.html', context)
