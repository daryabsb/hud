from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from src.products.models import Barcode, Product
from src.orders.models import PosOrderItem, PosOrder, PosOrderStatus
from src.pos.calculations import (create_order_item,)
from src.pos.utils import get_active_order, get_active_item
from src.orders.utils import context_factory
import after_response
from src.configurations.models import get_prop
layout_object = get_prop('layout')

update_active_order_template = 'pos/partials/order-detail.html'
update_items_list = 'pos/orders/items/list.html'
update_order_item_template = 'pos/renders/update-order-item.html'
update_order_list_template = 'pos/renders/update-order-list.html'
order_item_confirm_remove_template = 'pos/renders/order-item-with-confirm.html'
order_item_confirm_remove_template = 'pos/renders/order-item-with-confirm.html'

# New cotton updates
stanndard_order_item_add_template = 'cotton/orders/detail.html'
stanndard_activate_order_template = 'cotton/orders/order.html'
stanndard_order_update_calculations_template = 'cotton/orders/calculations.html'
update_orderitem_qty_template = 'pos/standard/renders/standard-item.html'


def change_quantity(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    quantity = request.POST.get("display", None)

    if quantity:
        item.quantity = quantity
        item.save()

    active_order = get_active_order(request.user)
    context = {"active_order": active_order, "item": item}
    return render(request, update_order_item_template, context)

@after_response.enable
def add_quantity_on_db(item_number):
    try:
        item = get_object_or_404(PosOrderItem, number=item_number)
        item.quantity += 1
        item.save()
    except Exception as e:
        print(f'Failed to update item quantity for item {item_number}: {e}')


@after_response.enable
def subtract_quantity_on_db(item_number):
    try:
        item = get_object_or_404(PosOrderItem, number=item_number)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except Exception as e:
        print(f'Failed to update item quantity for item {item_number}: {e}')

def add_quantity(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    item.quantity += 1  # Set quantity to the new value received from the client
    item.save()
    item.refresh_from_db()

    active_order = get_active_order(request.user)
    item = next((item for item in active_order['items'] if item['number'] == item_number), None)
    context = {"active_order": active_order,
               "order": active_order, "item": item}
    return render(request, update_orderitem_qty_template, context)


def subtract_quantity(request, item_number):

    item = get_object_or_404(PosOrderItem, number=item_number)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
        
    active_order = get_active_order(request.user)
    
    item = next((item for item in active_order['items'] if item['number'] == item_number), None)

    context = {"active_order": active_order,
               "order": active_order, "item": item or None}

    return render(request, update_orderitem_qty_template, context)

def focus_input(request):
    response = HttpResponse(status=204)
    response['Hx-Trigger'] = 'focus-input'
    return response

def remove_item(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    item.delete()

    active_order = get_active_order(request.user)
    context = {"active_order": active_order}
    # context = get_context(active_order)

    return render(request, update_order_list_template, context)

def delete_order_item_with_no_response(request, item_number):

    # try:
    import time
    time.sleep(2)
    item = get_object_or_404(PosOrderItem, number=item_number)
    item.delete()

    active_order = get_active_order(request.user)
    
    context = {"active_order": active_order}

    # response = HttpResponse(status=204)
    response = render(
        request, stanndard_order_update_calculations_template, context)
    response['Hx-Trigger'] = 'delete-order-item'

    return response

    # except Exception as e:
    #     print(f'Item does not exist: {e}')

def add_order_item(request):
    barcode_value = request.POST.get("barcode")
    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("qty", 1))

    active_order = get_active_order(request.user)

    if barcode_value:
        # Barcode method
        barcode = get_object_or_404(Barcode, value=barcode_value)
        product = barcode.product
    elif product_id:
        # Product ID method
        product = get_object_or_404(Product, id=product_id)
    else:
        return render(request, "error_template.html", {"error": "No product identifier provided"})

    item = PosOrderItem.objects.filter(
        order__number=active_order['number'], product=product
    ).first()

    if not item:
        item = create_order_item(
            request.user, active_order['number'], product, quantity
        )
    else:
        item.quantity += quantity
        item.save()

    active_order = get_active_order(request.user)
    context = {
        "active_order": active_order,
        "order": active_order,
        "item": item
    }

    context = context_factory(
        ["orders", "payment_types", "payment_type", "menus"],
        request.user, context=context
    )

    if layout_object['value'] == 'visual':
        context = context_factory(['products', 'groups'], context)
        return render(request, 'cotton/pos_base/pos_container.html', context)

    return render(request, 'cotton/pos_base/standard/container.html', context)
    # return render(request, stanndard_order_item_add_template, context)

def activate_order(request, order_number):
    # Fetch the order to activate
    print(f"Activating order: {order_number}")
    order_to_activate = get_object_or_404(PosOrder, number=order_number)

    print(f"order_to_activate: {order_to_activate.number}")
    # Get all enabled orders for the user
    orders = PosOrder.objects.filter(user=request.user, is_enabled=True)

    # Loop through each order and update the 'active' flag
    for order in orders:
        order.is_active = (order == order_to_activate)
        order.save()

    # Get the updated active order (assuming this function works as intended)
    active_order = get_active_order(request.user)

    context = {"order": active_order, "active_order": active_order}
    return render(request, stanndard_activate_order_template, context)

def order_discount(request, order_number):
    # Fetch the order to activate
    order = get_object_or_404(PosOrder, number=order_number)
    discount_sign = request.POST.get('discount-sign', None)
    discount = request.POST.get('display', None)
    
    order.discount = float(discount)
    order.discount_type = float(discount_sign)
    order.save()

    # Get the updated active order (assuming this function works as intended)
    active_order = get_active_order(request.user)

    context = {"order": active_order, "active_order": active_order}
    return render(request, stanndard_order_update_calculations_template, context)

def item_discount(request, item_number=None):
    # Fetch the order to activate
    item = get_object_or_404(PosOrderItem, number=item_number)
    discount_sign = request.POST.get('discount-sign', None)
    discount = request.POST.get('display', None)
    
    item.discount = float(discount)
    item.discount_type = float(discount_sign)
    item.save()
    
    print(f'submission = sign: {discount_sign}, value: {discount}')
    print(f"item to discount: {item.number}")

    active_order = get_active_order(request.user)
    item = next((item for item in active_order['items'] if item['number'] == item_number), None)
    context = {"active_order": active_order,
               "order": active_order, "item": item}
    return render(request, update_orderitem_qty_template, context)

from src.pos.forms import StatusForm

@require_POST
def update_status(request):
    
    form = StatusForm(request.POST)
    if form.is_valid():
        form.user = request.user
        form.save()
        return render(request, 'cotton/forms/order_status.html', form)
    
    # status_id = request.POST.get('status', None)
    # if status_id:
    #     active_order = PosOrder.objects.filter(is_active=True).first()
    #     status = get_object_or_404(PosOrderStatus, id=status_id)
    #     active_order.status = status
    #     active_order.save()
    #     context = {'status_form': UpdateOrderStatusForm(require_POST)}


from django.views.generic import View
       
# class StatusUpdateView(UpdateView):
#     model = PosOrder
#     form_class = StatusForm
#     template_name = 'cotton/forms/order_status.html'

class StatusUpdateView(View):
    template_name = 'cotton/buttons/order_status.html'

    def get(self, request, **kwargs):
        return self.render_form(request, kwargs['number'])

    def post(self, request, **kwargs):
        instance = get_object_or_404(PosOrder, number=kwargs['number'])
        status_form = StatusForm(request.POST, instance=instance)

        if status_form.is_valid():
            status_form.save()

        return self.render_form(request, kwargs['number'], form=status_form)

    def render_form(self, request, number, form=None):
        instance = get_object_or_404(PosOrder, number=number)
        status_form = form or StatusForm(instance=instance)
        active_order = get_active_order(user=request.user)

        context = {
            'status_form': status_form,
            'active_order': active_order,
        }
        return render(request, self.template_name, context)
