from decimal import Decimal
from django.shortcuts import render
from src.orders.models import PosOrder
from src.finances.models import PaymentType


from decimal import Decimal, InvalidOperation


def order_payment_change(request, order_number):
    # Fetch all payment types
    payment_types = PaymentType.objects.all()

    # Initialize paid amounts for each payment type
    paid = {pt.code: Decimal("0.00") for pt in payment_types}
    total_paid = Decimal("0.00")

    # Retrieve the order
    try:
        order = PosOrder.objects.get(number=order_number)
    except PosOrder.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)

    order_total = order.total

    # Parse paid amounts from the request
    for payment_type in payment_types:
        field_name = f"payment-amount-{payment_type.code}"
        raw_amount = request.GET.get(field_name, "0").replace(",", ".")

        try:
            paid_amount = Decimal(raw_amount)
        except InvalidOperation:
            paid_amount = Decimal("0.00")  # Fallback if invalid input

        # Update the paid dictionary and total paid
        paid[payment_type.code] = paid_amount
        total_paid += paid_amount

    # Calculate the remaining amount and change
    remaining = max(order_total - total_paid, Decimal("0.00"))
    change = max(total_paid - order_total, Decimal("0.00"))

    # Determine which payment type was modified (if any)
    payment_type_id = request.GET.get("payment_type", None)
    modified_payment_type = (
        PaymentType.objects.filter(
            id=payment_type_id).first() if payment_type_id else None
    )

    # Context for the template
    context = {
        "active_order": order,
        "payment_types": payment_types,
        "paid": paid,
        "remaining": remaining,
        "change": change,
        "modified_payment_type": modified_payment_type,
    }

    return render(request, "pos/payment/partials/change.html", context)
