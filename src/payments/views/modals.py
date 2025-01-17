from decimal import Decimal
from django.shortcuts import render
from src.orders.models import PosOrder


def order_payment_change(request, order_number):

    paid = request.GET.get('paid', 0)
    change = Decimal(paid)

    order = PosOrder.objects.get(number=order_number)

    if order:
        change = order.total - Decimal(paid)

    context = {
        'active_order': order,
        'change': change,
    }

    return render(request, 'pos/payment/partials/change.html', context)
