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
from src.pos2.mixins import AddOrderItemMixin, ItemUpdateMixin
from src.pos.forms import PosOrderForm
from src.pos2.forms import PosOrderItemForm, DefaultPosOrderItemForm
from src.pos2.utils import prepare_order_context


from src.pos2.const import active_order_template


class AddOrderItemView(AddOrderItemMixin, View):
    """View for adding new order items.

    This view uses the AddOrderItemMixin to handle adding new order items.
    It expects order_number to be provided in the URL kwargs.
    """
    template_name = active_order_template

    def post(self, request, **kwargs):
        barcode_value = request.POST.get("barcode", "").strip()
        quantity = int(request.POST.get("qty", 1))

        order_number = kwargs.get('order_number')
        active_order = get_active_order(request.user)
        item = None
        product = None

        # Create a form instance with the POST data
        form = DefaultPosOrderItemForm(request.POST)
        
        print('is_valid: ', request.POST)
        print('is_valid: ', form.is_valid())
        print('is_valid: ', form.errors)

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
                context = prepare_order_context(request, order_number, item)

                return render(request, active_order_template, context)

            except Barcode.DoesNotExist:
                # Not an exact barcode, fall through to search
                pass
        
        elif form.is_valid():
            # Temporarily save the form without committing to the DB
            item = form.save(commit=False)

            # Ensure the order is set (fallback to URL param if not in form)
            if not item.order and order_number:
                item.order = get_object_or_404(PosOrder, number=order_number)
            
            price = form.cleaned_data.get('price', None)
            if price is not None:
                item.price = price
            else:
                item.price = item.product.price  # fallback


            # Try to find an existing item (same order + product)
            existing_item = PosOrderItem.objects.filter(
                order=item.order, product=item.product
            ).first()

            if existing_item:
                # If item exists, just increment quantity
                existing_item.quantity += quantity
                existing_item.save()
                item = existing_item
            else:
                # For new item, complete additional required fields
                item.user = request.user
                item.quantity = quantity  # From POST, defaulted to 1

                # Example: Set price if not provided in form
                if not item.price:
                    item.price = item.product.default_price  # Or any logic you want

                # Save new item
                item.save()

            # Refresh order calculations
            item.order.refresh_cache()


            # Get the refreshed active order with updated calculations
            active_order = get_active_order(request.user)
            
            # Reuse the full order context
            context = prepare_order_context(request, order_number, item)

            return render(request, active_order_template, context)

        
        # If neither barcode nor form is valid, return the order context with form errors
        context = prepare_order_context(request, order_number)
        context['form'] = form
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
        context = prepare_order_context(request, order_number, item_instance)

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        # Use the post method from the mixin
        return super().post(request, **kwargs)


class UpdateItemQuantityView(ItemUpdateMixin, View):
    """View for updating item quantity."""
    
    def perform_update(self, request, item_instance):
        """Update the item quantity from POST data."""
        quantity = request.POST.get('quantity') or request.POST.get('display')
        if quantity:
            try:
                item_instance.quantity = float(quantity)
            except (ValueError, TypeError):
                pass  # Invalid quantity, ignore
    
    def post(self, request, **kwargs):
        return self.update_item_field(request, **kwargs)


class AddItemQuantityView(ItemUpdateMixin, View):
    """View for adding 1 to item quantity."""
    
    def perform_update(self, request, item_instance):
        """Add 1 to the item quantity."""
        item_instance.quantity += 1
    
    def post(self, request, **kwargs):
        return self.update_item_field(request, **kwargs)


class SubtractItemQuantityView(ItemUpdateMixin, View):
    """View for subtracting 1 from item quantity."""
    
    def perform_update(self, request, item_instance):
        """Subtract 1 from quantity or mark for deletion if quantity becomes 0."""
        if item_instance.quantity > 1:
            item_instance.quantity -= 1
        else:
            # Mark for deletion by setting a flag
            self._delete_item = True
    
    def post(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        item_number = kwargs.get('item_number')
        
        # Get the item instance
        item_instance = self.get_item_instance(item_number)
        
        # Check if we need to delete the item
        if item_instance.quantity <= 1:
            item_instance.delete()
            # Refresh order and render without the deleted item
            return self.refresh_order_and_render(request, order_number)
        else:
            # Use the standard update flow
            return self.update_item_field(request, **kwargs)


class UpdateItemDiscountView(ItemUpdateMixin, View):
    """View for updating item discount."""
    
    def perform_update(self, request, item_instance):
        """Update the item discount and discount type from POST data."""
        discount = request.POST.get('discount') or request.POST.get('display')
        discount_sign = request.POST.get('discount_type') or request.POST.get('discount-sign')
        
        if discount is not None:
            try:
                item_instance.discount = float(discount)
                if discount_sign is not None:
                    item_instance.discount_type = float(discount_sign)
            except (ValueError, TypeError):
                pass  # Invalid discount, ignore
    
    def post(self, request, **kwargs):
        return self.update_item_field(request, **kwargs)


class DeleteItemView(ItemUpdateMixin, View):
    """View for deleting an item."""
    
    def post(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        item_number = kwargs.get('item_number')
        
        # Get the item instance and delete it
        item_instance = self.get_item_instance(item_number)
        item_instance.delete()
        
        # Refresh order and render without the deleted item
        return self.refresh_order_and_render(request, order_number)



form = [
    'Meta', 
    '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', 
    '__getstate__', '__gt__', '__hash__', '__html__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', 
    '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
    '_bound_fields_cache', '_bound_items', '_clean_fields', '_clean_form', '_errors', '_get_validation_exclusions', '_meta', '_post_clean', 
    '_save_m2m', '_update_errors', '_validate_unique', '_widget_data_value', 
    'add_error', 'add_initial_prefix', 'add_prefix', 'as_div', 'as_p', 'as_table', 'as_ul', 'auto_id', 'base_fields', 
    'bound_field_class', 'changed_data', 'clean', 'data', 'declared_fields', 'default_renderer', 'empty_permitted', 
    'error_class', 'errors', 'field_order', 'fields', 'files', 'full_clean', 'get_context', 'get_initial_for_field', 
    'has_changed', 'has_error', 'hidden_fields', 'initial', 'instance', 'is_bound', 'is_multipart', 'is_valid', 
    'label_suffix', 'media', 'non_field_errors', 'order_fields', 'prefix', 'render', 'renderer', 'save', 'template_name', 
    'template_name_div', 'template_name_label', 'template_name_p', 'template_name_table', 'template_name_ul', 'use_required_attribute', 
    'validate_unique', 'visible_fields'
    ]