
from django.shortcuts import get_object_or_404, render
from src.orders.models.model_order_item import PosOrderItem
from src.products.models import Barcode, Product
from src.orders.utils import context_factory
from django.contrib.auth.decorators import login_required
from src.pos.calculations import create_order_item
from src.pos.utils import activate_order_and_deactivate_others as aod, get_active_order
from src.configurations.models import get_prop

layout_object = get_prop('layout')


def prepare_products_variannts(queryset=None):
    from src.products.models import Product, ProductGroup
    from collections import defaultdict
    if not queryset:
        queryset = Product.objects.all()

        grouped_products = defaultdict(lambda: defaultdict(list))

        for product in queryset:

            grouped_products[product.brand][product.name].append({
                'size': product.size,
                'dietary_option': product.dietary_option,
                'price': product.price,
                'stock': product.stock,
            })

@login_required
def pos_order2(request, number):
    active_order = aod(request.user, order_number=number)
    active_order.refresh_from_db()
    context = {
        'user': request.user,
        'active_order': active_order,
        'initialized': True,
    }

    context = context_factory(
        ["orders", "payment_types", "payment_type", "menus"], request.user, context=context)

    if layout_object.value == 'visual':
        context = context_factory(['products', 'groups'], context)
        return render(request, 'cotton/pos_base/pos_container.html', context)

    return render(request, 'cotton/pos_base/standard/container.html', context)


def add_order_item3(request):
    barcode_value = request.POST.get("barcode", "").strip()
    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("qty", 1))

    active_order = get_active_order(request.user)
    item = None
    product = None

    if barcode_value:
        # Try exact barcode match first
        try:
            barcode = Barcode.objects.get(value=barcode_value)
            product = barcode.product

            # Try to get existing order item
            item = PosOrderItem.objects.filter(
                order__number=active_order['number'], product=product
            ).first()

            if not item:
                item = create_order_item(request.user, active_order['number'], product, quantity)
            else:
                item.quantity += quantity
                item.save()

            # Full order context response (treat as Enter key)
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
                return render(request, 'cotton/pos_base/pos_container.html', context, content_type="text/html")

            return render(request, 'cotton/pos_base/standard/container.html', context, content_type="text/html")

        except Barcode.DoesNotExist:
            # Not an exact barcode, fall through to search
            pass

    elif product_id:
        product = get_object_or_404(Product, id=product_id)
        item = PosOrderItem.objects.filter(order__number=active_order['number'], product=product).first()
        if not item:
            item = create_order_item(request.user, active_order['number'], product, quantity)
        else:
            item.quantity += quantity
            item.save()

        # Reuse the full order context
        context = {
            "active_order": active_order,
            "order": active_order,
            "item": item
        }
        context = context_factory(
            ["orders", "payment_types", "payment_type", "menus"],
            request.user, context=context
        )

        return render(request, 'cotton/pos_base/standard/container.html', context)

    # 🔍 Search fallback
    products = Product.objects.filter(
        Q(name__icontains=barcode_value) |
        Q(barcode__value__icontains=barcode_value) |
        Q(parent_group__name__icontains=barcode_value) |
        Q(plu__icontains=barcode_value)
    ).distinct()[:20]

    context = {"products": products, "query": barcode_value}

    # Use HTMX Response Targets Extension to target dropdown
    response = render(request, "cotton/forms/barcode_input_dropdown.html", context)
    response["HX-Target"] = "#barcode-input-dropdown"
    return response