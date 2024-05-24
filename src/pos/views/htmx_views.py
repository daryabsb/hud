from django.shortcuts import get_object_or_404, render
from src.products.models import Barcode, Product
from src.orders.models import PosOrderItem
from src.pos.calculations import (create_order_item,)
from src.pos.utils import get_active_order

update_active_order_template = 'pos/partials/order-detail.html'
update_order_item_template = 'pos/renders/update-order-item.html'
order_item_confirm_remove_template = 'pos/renders/order-item-with-confirm.html'


def change_quantity(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    quantity = request.POST.get("display", None)

    if quantity:
        item.quantity = quantity
        item.save()

    active_order = get_active_order()
    context = {"active_order": active_order, "item": item}
    return render(request, update_active_order_template, context)


def add_quantity(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    item.quantity += 1  # Set quantity to the new value received from the client
    item.save()
    # item = recalculate_item(order_item=item)
    active_order = get_active_order()
    context = {"active_order": active_order, "item": item}
    return render(request, update_active_order_template, context)


def subtract_quantity(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        # item = recalculate_item(order_item=item)

        active_order = get_active_order()
        context = {"active_order": active_order, "item": item}
        return render(request, update_active_order_template, context)
    elif item.quantity == 1:

        active_order = get_active_order()
        context = {"active_order": active_order,
                   "item": item,
                   "confirm_remove": item.number}
        return render(request, update_active_order_template, context)


def remove_item(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    item.delete()

    active_order = get_active_order()
    context = {"active_order": active_order}
    # context = get_context(active_order)

    return render(request, update_active_order_template, context)


def add_item_with_barcode(request):
    barcode_value = request.POST.get("barcode", None)
    barcode = get_object_or_404(Barcode, value=barcode_value)
    active_order = get_active_order()

    item = PosOrderItem.objects.filter(
        user=request.user, order=active_order, product=barcode.product).first()
    if item:
        item.quantity += 1  # Set quantity to the new value received from the client
        item.save()
    else:
        item = create_order_item(
            request.user, active_order, barcode.product
        )

    active_order = get_active_order()
    context = {"active_order": active_order, "item": item}
    return render(request, update_active_order_template, context)


def add_order_item(request):
    product_id = request.POST.get('product_id', None)
    quantity = int(request.POST.get('quantity', 1))
    active_order = get_active_order()
    product = get_object_or_404(Product, id=product_id)

    item = PosOrderItem.objects.filter(
        order=active_order, product=product).first()

    if not item:
        item = create_order_item(
            request.user, active_order, product, quantity)
    else:
        item.quantity += quantity
        item.save()

    active_order = get_active_order()
    context = {"active_order": active_order, "item": item}

    return render(request, update_active_order_template, context)
