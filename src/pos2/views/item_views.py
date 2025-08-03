from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from src.orders.utils import context_factory
from src.products.models import Barcode, Product
from src.orders.models import PosOrderItem, PosOrder, PosOrderStatus
from src.pos.calculations import (create_order_item,)
from src.pos.utils import get_active_order
from src.pos2.mixins import AddOrderItemMixin

class AddOrderItemView(AddOrderItemMixin, View):
    """View for adding new order items.
    
    This view uses the AddOrderItemMixin to handle adding new order items.
    It expects order_number to be provided in the URL kwargs.
    """
    template_name = 'cotton/pos/order/index.html'
    
    def post(self, request, **kwargs):
        barcode_value = request.POST.get("barcode", "").strip()
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("qty", 1))

        order_number = kwargs.get('order_number')
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


class UpdateOrderItemView(AddOrderItemMixin, View):
    """View for updating existing order items.
    
    This view uses the AddOrderItemMixin to handle updating order items.
    It expects both order_number and item_number to be provided in the URL kwargs.
    """
    template_name = 'cotton/pos/order/index.html'
    
    def get(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        item_number = kwargs.get('item_number')
        
        # Get the item instance
        item_instance = self.get_item_instance(item_number)
        
        # Create a form with the item instance
        form = self.get_form(request, instance=item_instance)
        
        # Build context with the form and item
        active_order = get_active_order(request.user)
        context = context_factory(
            ["orders", "payment_types", "payment_type", "menus"],
            request.user,
            context={
                'form': form,
                'order': active_order,
                'active_order': active_order,
                'item': item_instance,
            }
        )
        
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        # Use the post method from the mixin
        return super().post(request, **kwargs)
