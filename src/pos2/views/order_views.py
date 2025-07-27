from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.views.generic import View
from src.orders.models import PosOrder
from src.pos.forms import StatusForm, PosOrderForm
from src.pos2.mixins import ActiveOrderViewsMixin
from src.pos.utils import get_active_order
from src.pos.forms import (
    DiscountAndTypeForm,
)

stanndard_order_update_calculations_template = 'cotton/orders/calculations.html'


class StatusUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['status']
    template_name = 'cotton/pos/order/index.html'


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
