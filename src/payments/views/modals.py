from decimal import Decimal
from django.shortcuts import render
from src.orders.models import PosOrder
from src.finances.models import PaymentType


def order_payment_change(request, order_number):
    payment_types = PaymentType.objects.all()
    paid = {}
    
    # Initialize paid amounts for each payment type
    for pt in payment_types:
        paid[pt.code] = Decimal('0.00')
    
    # Retrieve the payment amounts from the request
    for key, value in request.GET.items():
        if key.startswith('payment-amount-') and value:
            try:
                payment_type_id = key.replace('payment-amount-', '')
                amount = Decimal(str(value).replace(',', ''))
                # Find the payment type by ID and update the paid amount
                payment_type = PaymentType.objects.get(id=payment_type_id)
                paid[payment_type.code] = amount
            except (ValueError, PaymentType.DoesNotExist):
                continue
    
    # Calculate total paid and change
    total_paid = sum(paid.values())
    order = PosOrder.objects.get(number=order_number)
    change = total_paid - order.total if total_paid > order.total else Decimal('0.00')
    
    context = {
        'paid': paid,
        'total_paid': total_paid,
        'change': change,
        'order': order,
    }
    
    return render(request, 'cotton/pos/payment/partials/paid_change.html', context)
