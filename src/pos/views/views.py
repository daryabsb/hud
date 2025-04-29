from django.shortcuts import render
from src.orders.utils import context_factory
from django.contrib.auth.decorators import login_required
from src.stock.utils import get_paginated_stock_results
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from src.orders.models import get_orders
from src.stock.models import get_stocks
from src.configurations.utils import get_application_property
layout_object = get_application_property(name='layout')


def prepare_products_variannts(queryset=None):
    from src.products.models import Product, ProductGroup
    from collections import defaultdict
    if not queryset:
        queryset = Product.objects.all()

        grouped_products = defaultdict(lambda: defaultdict(list))

        for product in products:

            grouped_products[product.brand][product.name].append({
                'size': product.size,
                'dietary_option': product.dietary_option,
                'price': product.price,
                'stock': product.stock,
            })


@login_required
def pos_home(request, number=None):
    # if number:
    #     active_order = aod(request.user, order_number=number)
    # else:
    #     active_order = get_active_order(request.user)

    stock_context = get_paginated_stock_results(request)

    # orders = get_orders(user=request.user)
    orders = [order for order in get_orders(user=request.user)]
    active_order = next(
        (item for item in orders if item["is_active"] == True), None)
    if active_order is None:
        print("No active order found")

    context = {
        'orders': orders,
        # 'orders': [{'number': 'sales-18042025-1892'}, {'number': 'sales-30112024-0149'}],
        'active_order': active_order,
        'order': active_order,
        **stock_context,
    }

    context = context_factory(
        [
            "payment_types", "payment_type", "menus"], request.user, context=context)
    # context = {
    #     'active_order': active_order,
    #     'orders': [{'number': 'sales-18042025-1892'}, {'number': 'sales-30112024-0149'}]
    # }
    if request.htmx:
        # if layout_object.value == 'visual':
        #     context = context_factory(['products', 'groups'], context)
        #     return render(request, 'cotton/pos_base/pos_container.html', context)

        return render(request, 'cotton/pos_base/standard/container.html', context)

    # if layout_object.value == 'visual':
    #     context = context_factory(['products', 'groups'], context)
    #     return render(request, 'cotton/pos_base/visual/index.html', context)
    return render(request, 'cotton/pos_base/standard/index.html', context)


@login_required
def pos_order(request, number):
    active_order = aod(request.user, order_number=number)
    active_order.refresh_from_db()
    context = {
        'user': request.user,
        'active_order': active_order,
        'initialized': True,
    }

    context = context_factory(
        ["orders", "payment_types", "payment_type", "menus"], request.user, context=context)

    if layout_object.value == 'visual':
        context = context_factory(['products', 'groups'], context)
        return render(request, 'cotton/pos_base/pos_container.html', context)

    return render(request, 'cotton/pos_base/standard/container.html', context)
