from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.views.generic import View
from src.pos.forms import StatusForm, PosOrderForm
from src.orders.models import PosOrder
from src.pos.utils import get_active_order
from src.pos.forms import (
    DiscountAndTypeForm,
    )

stanndard_order_update_calculations_template = 'cotton/orders/calculations.html'


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
                {'Meta': type('Meta', (self.form_class.Meta,), {'fields': self.form_fields})}
            )
        return form_class(data, instance=instance)

    def render_form(self, request, number, form=None):
        instance = self.get_instance(number)
        form = form or self.get_form(request, instance=instance)
        active_order = get_active_order(user=request.user)

        context = {
            'form': form,
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


class StatusUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['status']
    template_name = 'cotton/buttons/order_status.html'


class CommentUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['note']
    template_name = 'cotton/buttons/pos/comment.html'


class InternalNoteUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['internal_note']
    template_name = 'cotton/buttons/pos/internal_note.html'


class DiscountUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['discount', 'discount_type']
    template_name = 'cotton/orders/calculations.html'
    

class DiscountAndTypeUpdateView(UpdateView):
    model = PosOrder
    form_class = DiscountAndTypeForm
    template_name = 'posorder/partials/field_update_form.html'

    def form_valid(self, form):
        self.object = form.save()
        active_order = get_active_order(self.request.user)
        return render(self.request, stanndard_order_update_calculations_template, {
            'active_order': active_order,
        })

    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            'form': form,
            'field_name': 'discount_and_type'
        })