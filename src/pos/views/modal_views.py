
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404, render
from src.products.models import Product
from src.orders.models import PosOrder, PosOrderItem
from src.accounts.models import Customer
from src.finances.models import PaymentType


def modal_product(request, number):
    print('ID = ', number)
    active_order = PosOrder.objects.filter(is_active=True).first()
    item = get_object_or_404(PosOrderItem, number=number)
    product = item.product

    if product:
        context = {
            "item": item,
            "product": product,
            "active_order": active_order
        }
        return render(request, 'pos/modals/product-modal.html', context)


def modal_calculator(request):
    import json
    is_ajax = request.GET.get('is_ajax', False)
    div_class = request.GET.get('div-class', '')
    el_id = request.GET.get('el-id', '')
    url = request.GET.get('url', '')
    template_name = request.GET.get('template-name', '')
    digits = [[7, 8, 9, '/'], [4, 5, 6, '*'],
              [1, 2, 3, '-'], [0, '.', '=', '+'],]
    context = {
        "calc_on": True,
        "is_ajax": is_ajax,
        "div_class": div_class,
        "el_id": el_id,
        "template_name": template_name,
        "url": url,
        "digits": digits,
    }

    return render(request, 'pos/modals/calculator-modal.html', context)


def modal_keyboard(request):
    from src.pos.utils import qwerty
    is_ajax = request.GET.get('is_ajax', False)
    div_class = request.GET.get('div-class', '')
    el_id = request.GET.get('el-id', '')
    url = request.GET.get('url', '')
    template_name = request.GET.get('template-name', '')

    # Numeric (calculator) layout
    digits = [
        [7, 8, 9, '/'],
        [4, 5, 6, '*'],
        [1, 2, 3, '-'],
        [0, '.', '=', '+'],
    ]

    # QWERTY keyboard layout
    # qwerty = [
    #     ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    #     ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    #     ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    # ]

    context = {
        "calc_on": True,
        "is_ajax": is_ajax,
        "div_class": div_class,
        "el_id": el_id,
        "template_name": template_name,
        "url": url,
        "digits": digits,
        "qwerty": qwerty,  # Include the QWERTY layout
    }

    return render(request, 'pos/modals/keyboard-modal.html', context)


def calculate(request):
    from django.http import JsonResponse
    calculation = request.POST.get('display', '')
    # Process the calculation as needed, e.g., log it, store it, etc.
    print("calculation = ", calculation)
    return JsonResponse({'message': calculation})


def add_digit(request):
    if request.method == 'POST':
        current_value = request.POST.get('display', '')
        digit = request.POST.get('digit', '')
        new_value = current_value + digit
        return render(request, 'components/calculator/input_display.html', {'new_value': new_value})
    return render(request, 'keypad.html', {'error': 'Invalid request'})


@login_required
@require_POST
def add_order_comment(request, order_number):
    if order_number:
        order = get_object_or_404(PosOrder, number=order_number)

    comment = request.POST.get('comment', None)

    if comment:
        order.note = comment
        order.save()

    return render(request, 'pos/buttons/render-order-comment.html')


@login_required
@require_GET
def add_order_customer(request, order_number):
    from src.pos.utils import activate_order_and_deactivate_others as aod
    if order_number:
        order = get_object_or_404(PosOrder, number=order_number)

    customer = request.GET.get('customer', None)

    if customer:
        instance = Customer.objects.get(pk=customer)
        order.customer = instance
        order.save()
        return render(request, 'pos/buttons/active-order-customer.html', {'active_order': order})
    else:
        return JsonResponse({'error': 'No customer selected'})


@login_required
@require_GET
def add_order_payment(request, order_number):
    from src.pos.utils import activate_order_and_deactivate_others as aod

    payment_type_id = request.GET.get('payment-type', None)

    if payment_type_id:
        payment_type = get_object_or_404(PaymentType, id=payment_type_id)

    if order_number:
        order = get_object_or_404(PosOrder, number=order_number)

    customer = request.GET.get('customer', None)

    if customer:
        instance = Customer.objects.get(pk=customer)
        order.customer = instance
        order.save()
        return render(request, 'pos/buttons/active-order-customer.html', {'active_order': order})
    else:
        return JsonResponse({'error': 'No customer selected'})
