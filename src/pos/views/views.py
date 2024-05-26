from django.shortcuts import render
from src.products.models import Product, ProductGroup
from src.orders.models import PosOrder
from src.pos.utils import activate_order_and_deactivate_others as aod
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def pos_home(request, id=None):
    user = request.user
    active_order = aod(user, id)

    product_groups = ProductGroup.objects.filter(parent__isnull=True)
    pos_orders = PosOrder.objects.all()
    products = Product.objects.all()

    context = {
        "active_order": active_order,
        "groups": product_groups,
        "products": products,
        "orders": pos_orders,
    }
    return render(request, 'pos/pos-home.html', context)
