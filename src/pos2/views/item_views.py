from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from src.orders.utils import context_factory
from src.products.models import Barcode, Product
from src.orders.models import PosOrderItem, PosOrder, PosOrderStatus
from src.pos.calculations import (create_order_item,)
from src.pos.utils import get_active_order

class AddOrderItemView(View):
    def post(self, request):
        barcode_value = request.POST.get("barcode", "").strip()
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("qty", 1))

        active_order = get_active_order(request.user)
        item = None
        product = None
        order_number = active_order['number'] if active_order else None

        if barcode_value:
            # Try exact barcode match first
            try:
                barcode = Barcode.objects.get(value=barcode_value)
                product = barcode.product

                # Try to get existing order item
                item = PosOrderItem.objects.filter(
                    order__number=order_number, product=product
                ).first()

                if not item:
                    item = create_order_item(
                        request.user, order_number, product, quantity)
                else:
                    item.quantity += quantity
                    item.save()

                # Refresh the order to get updated calculations
                if order_number:
                    order = PosOrder.objects.get(number=order_number)
                    order.refresh_cache()

                # Get the refreshed active order with updated calculations
                active_order = get_active_order(request.user)

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

                # if layout_object['value'] == 'visual':
                #     context = context_factory(['products', 'groups'], context)
                #     return render(request, 'cotton/pos_base/pos_container.html', context, content_type="text/html")

                return render(request, 'cotton/pos/order/index.html', context)

            except Barcode.DoesNotExist:
                # Not an exact barcode, fall through to search
                pass

        elif product_id:
            product = get_object_or_404(Product, id=product_id)
            item = PosOrderItem.objects.filter(
                order__number=order_number, product=product).first()
            if not item:
                item = create_order_item(
                    request.user, order_number, product, quantity)
            else:
                item.quantity += quantity
                item.save()

            # Refresh the order to get updated calculations
            if order_number:
                order = PosOrder.objects.get(number=order_number)
                order.refresh_cache()

            # Get the refreshed active order with updated calculations
            active_order = get_active_order(request.user)

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
