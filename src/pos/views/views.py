from django.shortcuts import get_object_or_404, render
from src.orders.utils import context_factory
from django.contrib.auth.decorators import login_required
from src.stock.utils import get_paginated_stock_results
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from src.orders.models import get_orders, PosOrder
from src.accounts.models import get_customers
from src.configurations.models import get_prop
layout_object = get_prop('layout')


@login_required
def pos_home(request, number=None):
    
    orders = get_orders(user=request.user)
    active_order = get_active_order(request.user)

    if active_order is None:
        print("No active order found")

    context = {
        'orders': orders,
        # 'orders': [{'number': 'sales-18042025-1892'}, {'number': 'sales-30112024-0149'}],
        'active_order': active_order,
        # **stock_context,
    }
    return render(request, 'cotton/pos_home.html', context)

@login_required
def pos_order(request, number):
    from src.pos.forms import PosOrderForm
    orders = [order for order in get_orders(user=request.user)]
    order = get_object_or_404(PosOrder, number=number)
    form = PosOrderForm(instance=order)
    customers = get_customers(user=request.user)
    
    print(f'customers: {customers}')
        
    if number:
        # active_order = next((item for item in orders if item["is_active"] == True), None)
        active_order = aod(request.user, order_number=number)
    else:
        active_order = get_active_order(request.user)

    # stock_context = get_paginated_stock_results(request)

    # orders = get_orders(user=request.user)
    if active_order is None:
        print("No active order found")

    context = {
        'orders': orders,
        'form': form,
        'customers': customers,        
        # 'orders': [{'number': 'sales-18042025-1892'}, {'number': 'sales-30112024-0149'}],
        'active_order': active_order,
        'order': active_order,
        # **stock_context,
    }

    context = context_factory(
        [
            "payment_types", "payment_type", "menus"], request.user, context=context)
    # context = {
    #     'active_order': active_order,
    #     'orders': [{'number': 'sales-18042025-1892'}, {'number': 'sales-30112024-0149'}]
    # }
    if request.htmx:
        if layout_object['value'] == 'visual':
            context = context_factory(['products', 'groups'], context)
            return render(request, 'cotton/pos_base/pos_container.html', context)

        return render(request, 'cotton/pos_base/standard/container.html', context)

    if layout_object['value'] == 'visual':
        context = context_factory(['products', 'groups'], context)
        return render(request, 'cotton/pos_base/visual/index.html', context)
    return render(request, 'cotton/pos_base/standard/index.html', context)