from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from src.orders.utils import context_factory
from src.products.models import Barcode, Product
from src.orders.models import PosOrderItem, PosOrder, get_orders
from src.pos.calculations import (create_order_item,)
from src.pos.utils import get_active_order
from src.accounts.models import get_customers
from src.configurations.models import get_prop
from src.finances.models.models_payment_type import get_tree_nodes as get_payment_types
from src.configurations.models import get_menus
from src.pos2.mixins import AddOrderItemMixin
from src.pos.forms import PosOrderForm


from src.pos2.const import active_order_template


class AddOrderItemView(AddOrderItemMixin, View):
    """View for adding new order items.

    This view uses the AddOrderItemMixin to handle adding new order items.
    It expects order_number to be provided in the URL kwargs.
    """
    template_name = active_order_template

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
                order_instance = get_object_or_404(
                    PosOrder, number=active_order['number'])

                # Full order context response (treat as Enter key)
                context = {
                    'orders': get_orders(user=request.user),
                    'form': PosOrderForm(instance=order_instance),
                    'menus': get_menus(),
                    'payment_types': get_payment_types(),
                    'payment_type': get_payment_types()[0],
                    'customers': get_customers(user=request.user),
                    "active_order": active_order,
                    "order": active_order,
                    "item": item
                }

                # if layout_object['value'] == 'visual':
                #     context = context_factory(['products', 'groups'], context)
                #     return render(request, 'cotton/pos_base/pos_container.html', context, content_type="text/html")

                return render(request, active_order_template, context)

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
            order_instance = get_object_or_404(
                PosOrder, number=active_order['number'])

            # Reuse the full order context
            context = {
                'orders': get_orders(user=request.user),
                'form': PosOrderForm(instance=order_instance),
                'menus': get_menus(),
                'payment_types': get_payment_types(),
                'payment_type': get_payment_types()[0],
                'customers': get_customers(user=request.user),
                "active_order": active_order,
                "order": active_order,
                "item": item
            }

            return render(request, active_order_template, context)


class UpdateOrderItemView(AddOrderItemMixin, View):
    """View for updating existing order items.

    This view uses the AddOrderItemMixin to handle updating order items.
    It expects both order_number and item_number to be provided in the URL kwargs.
    """
    template_name = active_order_template

    def get(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        item_number = kwargs.get('item_number')

        # Get the item instance
        item_instance = self.get_item_instance(item_number)

        # Create a form with the item instance
        form = self.get_form(request, instance=item_instance)

        # Build context with the form and item
        active_order = get_active_order(request.user)
        order_instance = get_object_or_404(
            PosOrder, number=active_order['number'])

        # Reuse the full order context
        context = {
            'orders': get_orders(user=request.user),
            'form': PosOrderForm(instance=order_instance),
            'menus': get_menus(),
            'payment_types': get_payment_types(),
            'payment_type': get_payment_types()[0],
            'customers': get_customers(user=request.user),
            "active_order": active_order,
            "order": active_order,
            "item": item
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        # Use the post method from the mixin
        return super().post(request, **kwargs)
