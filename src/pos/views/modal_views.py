
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404, render
from src.products.models import Product
from src.orders.models import PosOrder, PosOrderItem
from django.core.paginator import Paginator
from src.accounts.models import Customer
from src.finances.models import PaymentType
from src.pos.utils import get_active_order, activate_order_and_deactivate_others as aod
from src.stock.models import Stock, StockControl
from django.db.models import OuterRef, Subquery, BooleanField, ExpressionWrapper, F

modal_item_template = 'cotton/modals/pos_item.html'
modal_product_template = 'cotton/modals/product.html'


def modal_order_item(request, number):
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
        return render(request, modal_item_template, context)


def modal_product(request, id):
    print('ID = ', id)
    active_order = get_active_order(request.user)
    product = get_object_or_404(Product, id=id)

    context = {
        "product": product,
        "active_order": active_order
    }
    return render(request, modal_product_template, context)


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


def calculator_modal(request):
    is_ajax = request.GET.get('is_ajax', True)
    div_class = request.GET.get('div-class', '')
    el_id = request.GET.get('el-id', '')
    discount_type = request.GET.get('discount_type', '0')
    url = request.GET.get('url', '')
    kamal = request.GET.get('kamal', '')
    template_name = request.GET.get('template-name', '')
    print(f'kamal: {kamal}')
    print(f'el_id: {el_id}')
    print(f'is_ajax: {is_ajax}')
    digits = [
        [7, 8, 9], [4, 5, 6],
        [1, 2, 3], 
        ['.', 0, '=']
    ]
    context = {
        "calc_on": True,
        "is_ajax": is_ajax,
        "div_class": div_class,
        "el_id": el_id,
        "discount_type": discount_type,
        "template_name": template_name,
        "url": url,
        "digits": digits,
    }

    return render(request, 'cotton/modals/calculator.html', context)


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


def toggle_modal_comment(request, order_number):
    order = get_object_or_404(PosOrder, number=order_number)
    active_order = get_active_order(request.user)

    return render(request, 'cotton/modals/comment.html', {
        'order': order,
        'active_order': active_order,
    })


@login_required
@require_POST
def add_order_comment(request, order_number):
    if order_number:
        order = get_object_or_404(PosOrder, number=order_number)
    else:
        order = get_active_order(request.user)

    print("View called!sss")

    comment = request.POST.get('comment', '')
    # if comment:
    order.note = comment
    order.save()

    active_order = get_active_order(request.user)

    context = {
        "active_order": active_order,
        "badge": "?",
    }

    return render(request, 'cotton/buttons/pos/comment.html', context)


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
def pos_search_modal(request):
    from src.stock.filters import StockFilter
    from src.stock.utils import get_paginated_stock_results
    from src.orders.models import get_orders
    from src.stock.models import get_stocks
    stock_controls = StockControl.objects.filter(
        product=OuterRef('product')).select_related('customer', 'user')

    orders = get_orders(user=request.user)
    active_order = next(
        (item for item in orders if item["is_enabled"] == True), None)
    if active_order is None:
        print("No active order found")

    stock_context = get_paginated_stock_results(request)

    # queryset = Stock.objects.annotate(
    #     preferred_quantity=Subquery(
    #         stock_controls.values('preferred_quantity')[:1]),
    #     is_low_stock_warning_enabled=Subquery(
    #         stock_controls.values('is_low_stock_warning_enabled')[:1]),
    #     low_stock_warning_quantity=Subquery(
    #         stock_controls.values('low_stock_warning_quantity')[:1]),
    #     customer=Subquery(stock_controls.values('customer__name')[:1]),
    # ).select_related('warehouse', 'user')

    # stock_filter = StockFilter(request.GET, queryset=queryset)

    # # Pagination
    # page_number = request.GET.get("page", 1)
    # paginator = Paginator(stock_filter.qs, 5)
    # page_obj = paginator.get_page(page_number)

    context = {
        'active_order': active_order,
        **stock_context,

    }

    is_next = request.GET.get("is_next") == "1"
    if is_next:
        return render(request, 'cotton/modals/search/products/rows.html', context)
    return render(request, 'cotton/modals/search/index.html', context)
