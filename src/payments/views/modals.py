from decimal import Decimal
from django.shortcuts import render
from src.orders.models import PosOrder


def order_payment_change(request, order_number):

    paid = request.GET.get('cash', [])
    paid2 = request.GET.get('paid2', [])

    print("Paid: ", paid)
    print("Paid2: ", paid2)

    change = Decimal(paid) if paid else Decimal(0.00)

    payment_type = request.GET.get('payment_type', None)

    paid = Decimal(paid) if paid else Decimal(0.00)

    if payment_type:
        print("Payment type: ", payment_type)

    order = PosOrder.objects.get(number=order_number)

    if order:
        change = paid - order.total
    if change > 0.00:
        print("It is bigger than 0")
    else:
        print("It is smaller than 0")

    paid = {
        'CASH': '',
        'CC': '',
        'DC': '',
        'CHEQ': '',
        'VOU': '',
        'GC': '',
    }

    context = {
        'active_order': order,
        'paid': paid,
        'change': change,
    }

    return render(request, 'pos/payment/partials/change.html', context)
