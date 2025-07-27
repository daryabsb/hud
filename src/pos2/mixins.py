from django.shortcuts import get_object_or_404, render
from src.orders.models import PosOrder, get_orders
from src.pos.forms import PosOrderForm
from src.pos.utils import get_active_order
from src.configurations.models import get_menus


class ActiveOrderViewsMixin:
    model = PosOrder
    form_class = PosOrderForm
    template_name = None
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
        orders = get_orders(user=request.user)
        active_order = get_active_order(user=request.user)

        context = {
            'orders': orders,
            'menus': get_menus(),
            'form': form,
            'order': active_order,
            'active_order': active_order,
        }
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
