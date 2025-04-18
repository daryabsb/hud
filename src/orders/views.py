from django.shortcuts import render
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from src.orders.utils import create_new_order
from django.contrib.auth.decorators import login_required

from src.orders.const import get_template_for_view

# Create your views here.
stanndard_activate_order_template = 'cotton/orders/order.html'


@login_required
def add_new_order(request):
    template = get_template_for_view()

    order = create_new_order(request.user)
    active_order = aod(request.user, order_number=order.number)

    context = {"order": active_order, "active_order": active_order}
    return render(request, template, context)


@login_required
def delete_active_order(request):
    template = get_template_for_view()

    active_order = get_active_order()
    active_order.delete()
    aod(request.user, activate=True)

    context = {"order": active_order, "active_order": active_order}
    return render(request, template, context)
