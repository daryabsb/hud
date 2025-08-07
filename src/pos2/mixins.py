from django.shortcuts import get_object_or_404, render
from src.orders.models import PosOrder, PosOrderItem, get_orders
from src.pos2.forms import PosOrderForm, PosOrderItemForm
from src.pos.utils import get_active_order
from src.configurations.models import get_menus
from src.finances.models.models_payment_type import get_tree_nodes as get_payment_types
from src.accounts.models import get_customers
from src.pos2.utils import prepare_order_context

from src.pos2.const import active_order_template


class ActiveOrderViewsMixin:
    model = PosOrder
    form_class = PosOrderForm
    template_name = active_order_template
    form_fields = None  # Allows specifying which fields to include

    def get_instance(self, number):
        return get_object_or_404(self.model, number=number)

    def get_form(self, request, instance=None, data=None):
        """Instantiate the form with specific fields if form_fields is set."""
        form_class = self.form_class
        if self.form_fields:
            # Limit the form to the specified fields
            form_class = type(
                f"Partial{self.form_class.__name__}",
                (self.form_class,),
                {'Meta': type('Meta', (self.form_class.Meta,),
                              {'fields': self.form_fields})}
            )
        return form_class(data, instance=instance)

    def render_form(self, request, number, form=None):
        instance = self.get_instance(number)
        form = form or self.get_form(request, instance=instance)
        
        # Use the utility function to prepare the context
        context = prepare_order_context(request, number)
        
        # Add the form to the context
        context['form'] = form
        
        return render(request, self.template_name, context)

    def get(self, request, **kwargs):
        return self.render_form(request, kwargs['number'])

    def post(self, request, **kwargs):
        instance = self.get_instance(kwargs['number'])
        form = self.get_form(request, instance=instance, data=request.POST)
        note = request.POST.get('note', None)
        print(f'note: {note}, is_valid: {form.is_valid()}')
        if form.is_valid():
            form.save()

        return self.render_form(request, kwargs['number'], form=form)


class AddOrderItemMixin:
    model = PosOrderItem
    form_class = PosOrderItemForm
    form_fields = None  # Allows specifying which fields to include
    template_name = active_order_template  # Use active order template by default

    def get_order_instance(self, order_number):
        return get_object_or_404(PosOrder, number=order_number)
    
    def get_item_instance(self, item_number=None):
        if item_number:
            return get_object_or_404(PosOrderItem, number=item_number)
        return None

    def get_form(self, request, instance=None, data=None):
        """Instantiate the form with specific fields if form_fields is set."""
        form_class = self.form_class
        if self.form_fields:
            # Limit the form to the specified fields
            form_class = type(
                f"Partial{self.form_class.__name__}",
                (self.form_class,),
                {'Meta': type('Meta', (self.form_class.Meta,),
                              {'fields': self.form_fields})}
            )
        return form_class(data, instance=instance)

    def render_order_form(self, request, order_number, item_number=None, form=None):
        order_instance = self.get_order_instance(order_number)
        item_instance = self.get_item_instance(item_number) if item_number else None
        form = form or self.get_form(request, instance=item_instance)
        
        # Use the utility function to prepare the context
        context = prepare_order_context(request, order_number, item_instance)
        
        # Add the form to the context
        context['form'] = form
        
        return render(request, self.template_name, context)

    def get(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        item_number = kwargs.get('item_number')
        return self.render_order_form(request, order_number, item_number)

    def post(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        item_number = kwargs.get('item_number')
        
        # Get the order instance
        order_instance = self.get_order_instance(order_number)
        
        # Get the item instance if updating, otherwise None for new item
        item_instance = self.get_item_instance(item_number)
        
        # Create or update the item
        form = self.get_form(request, instance=item_instance, data=request.POST)
        
        if form.is_valid():
            item = form.save(commit=False)
            
            # Set order if it's a new item
            if not item_number:
                item.order = order_instance
                item.user = request.user
            
            item.save()
            
            # Refresh the order cache to update calculations
            order_instance.refresh_cache()
        
        # Re-fetch the active order to get updated calculations
        active_order = get_active_order(request.user)
        
        # Build context with updated data using the utility function
        context = prepare_order_context(request, order_number, item_instance)
        context['form'] = form
        
        return render(request, self.template_name, context)
