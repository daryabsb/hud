from django.shortcuts import render
from django.views.generic.edit import UpdateView
from src.orders.models import PosOrder
from src.pos.utils import get_active_order
from src.pos.forms import (
    DiscountAndTypeForm,
    )

stanndard_order_update_calculations_template = 'cotton/orders/calculations.html'


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