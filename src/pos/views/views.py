from django.shortcuts import render
from collections import defaultdict
from src.products.models import Product, ProductGroup
from src.orders.models import PosOrder
from src.pos.utils import activate_order_and_deactivate_others as aod
from django.contrib.auth.decorators import login_required
from src.configurations.models import ApplicationProperty
# Create your views here.


def prepare_products_variannts(queryset: Product = None):
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
    print('Last Activity: ', request.session['last_activity'])
    user = request.user
    active_order = aod(user, number)
    layout_object = ApplicationProperty.objects.get(name='layout')

    print(layout_object.value)

    product_groups = ProductGroup.objects.filter(parent__isnull=True)
    pos_orders = PosOrder.objects.all()
    products = Product.objects.all()

    context = {
        "active_order": active_order,
        "groups": product_groups,
        "products": products,
        "orders": pos_orders,
    }
    if layout_object.value == 'standard':
        return render(request, 'pos/standard/pos-home.html', context)
    return render(request, 'pos/visual/pos-home.html', context)
