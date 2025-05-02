
from django.shortcuts import render
from src.orders.utils import context_factory
from django.contrib.auth.decorators import login_required
from src.pos.utils import activate_order_and_deactivate_others as aod

from src.configurations.models import get_prop

layout_object = get_prop('layout')


def prepare_products_variannts(queryset=None):
    from src.products.models import Product, ProductGroup
    from collections import defaultdict
    if not queryset:
        queryset = Product.objects.all()

        grouped_products = defaultdict(lambda: defaultdict(list))

        for product in queryset:

            grouped_products[product.brand][product.name].append({
                'size': product.size,
                'dietary_option': product.dietary_option,
                'price': product.price,
                'stock': product.stock,
            })

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
