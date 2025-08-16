from decimal import Decimal
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404, render, reverse

from src.orders.models import PosOrder, PosOrderItem
from src.finances.models import PaymentType
from src.pos2.const import active_order_template
from src.pos2.utils import prepare_order_context
from src.documents.utils import create_document_from_order as cdo


@login_required
@require_POST
def pay_order_and_close(request, order_number):
    # Process payment logic
    order = get_object_or_404(PosOrder, number=order_number)
    document, next_order = cdo(order)

    if next_order:
        number = next_order.number
    context = prepare_order_context(request, number)
    redirect_url = reverse(
        'pos2:pos-order', kwargs={'number': number})
    # Empty response (HTMX will handle redirect)
    response = HttpResponse(status=204)
    response['HX-Redirect'] = redirect_url  # HTMX-specific redirect header
    return response


@login_required
@require_GET
def add_order_payment(request, order_number):
    from src.pos.utils import activate_order_and_deactivate_others as aod
    from src.finances.models import PaymentType

    print('View order payment called!!!')

    payment_type_id = request.GET.get('payment-type', None)

    if payment_type_id:
        payment_type = get_object_or_404(PaymentType, id=payment_type_id)
    else:
        payment_type = PaymentType.objects.first()

    if order_number:
        order = get_object_or_404(PosOrder, number=order_number)
    payment_types = PaymentType.objects.filter(is_enabled=True)
    # customer = request.GET.get('customer', None)

    # if customer:
    #     instance = Customer.objects.get(pk=customer)
    #     order.customer = instance
    #     order.save()
    #     return render(request, 'pos/buttons/active-order-customer.html', {'active_order': order})
    # else:
    #     return JsonResponse({'error': 'No customer selected'})
    remaining = order.total
    context = {
        'payment_type': payment_type,
        'active_order': order,
        'remaining': order.total,
        'payment_types': payment_types,
        'change': Decimal(0)
    }
    return render(request, 'cotton/pos/payment/payment_modal.html', context)
