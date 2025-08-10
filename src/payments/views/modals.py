from decimal import Decimal
from django.shortcuts import render
from src.orders.models import PosOrder
from src.finances.models import PaymentType


def order_payment_change(request, order_number):
    payment_types = PaymentType.objects.all()
    paid = {
        'CASH': Decimal(0.00),
        'CC': Decimal(0.00),
        'DC': Decimal(0.00),
        'CHEQ': Decimal(0.00),
        'VOU': Decimal(0.00),
        'GC': Decimal(0.00),
    }
    
    # Retrieve the payment amounts from the request
    # for payment_type in payment_types:
    #     pid = f"payment-amount-{payment_type.code}"
    #     p_amount = request.GET.get(pid, None)
    #     if p_amount:
    #         p_amount = p_amount.replace(',', '')
    #         paid[payment_type.code] = Decimal(p_amount) if p_amount else Decimal(0.00)
    # total_paid = sum(paid.values())
    
    pid = f"payment-amount-CASH"
    p_amount = request.GET.get(pid, None)
    if p_amount:
        p_amount = p_amount.replace(',', '')
        paid = Decimal(p_amount) if p_amount else Decimal(0.00)
    total_paid = paid
    print(total_paid)

    # Calculate the total paid amount

    # Retrieve the order
    order = PosOrder.objects.get(number=order_number)
    order_total = order.total

    # Calculate the remaining amount and change
    remaining = order_total - total_paid
    change = total_paid - order_total if total_paid > order_total else Decimal(0.00)

    context = {
        'active_order': order,
        'paid': total_paid,
        'change': change,
        'remaining': remaining,
        'payment_types': payment_types,
    }

    return render(request, 'cotton/pos/payment/partials/change.html', context)
