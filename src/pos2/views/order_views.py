from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.views.generic import View
from src.orders.models import PosOrder
from src.pos.forms import StatusForm, PosOrderForm
from src.pos2.mixins import ActiveOrderViewsMixin
from src.pos.utils import get_active_order
from src.pos2.utils import prepare_order_context
from src.pos.forms import (
    DiscountAndTypeForm,
)

stanndard_order_update_calculations_template = 'cotton/orders/calculations.html'
active_order_template = 'cotton/pos/order/active_order.html'


class StatusUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['status']

class CommentUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['note']

class InternalNoteUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['internal_note']

class DiscountUpdateView(ActiveOrderViewsMixin, View):
    form_fields = ['discount', 'discount_type']

class GenericOrderUpdateView(ActiveOrderViewsMixin, View):
    """
    A flexible view that can handle updating any field or combination of fields
    in the PosOrder model. The fields to update are determined by the request data.
    
    This view can be used in two ways:
    1. By including the fields to update in the POST data
    2. By specifying the fields in the URL query parameters (fields=status,note,discount)
    """
    template_name = 'cotton/pos/forms/generic_order_form.html'
    
    def get_form_fields(self, request):
        """
        Determine which fields to include in the form based on the request data.
        Only include fields that are present in the request and in POS_FORM_FIELDS.
        """
        from src.pos.const import POS_FORM_FIELDS
        
        # Check if fields are specified in the query parameters
        fields_param = request.GET.get('fields')
        if fields_param:
            # Split the comma-separated list of fields
            field_names = [field.strip() for field in fields_param.split(',') 
                          if field.strip() in POS_FORM_FIELDS]
            if field_names:
                return field_names
        
        # If no fields in query params or they were invalid, check POST data
        if request.method == 'POST':
            field_names = [field for field in request.POST.keys() 
                          if field in POS_FORM_FIELDS and field != 'csrfmiddlewaretoken']
            if field_names:
                return field_names
        
        # If no valid fields found, return a default set of fields
        # This can be customized based on your requirements
        return ['status', 'note']
    
    def get(self, request, **kwargs):
        # For GET requests, set form_fields based on query parameters
        self.form_fields = self.get_form_fields(request)
        return super().get(request, **kwargs)
    
    def post(self, request, **kwargs):
        # Dynamically set form_fields based on the request data
        self.form_fields = self.get_form_fields(request)
        
        # Use the standard post method from the mixin
        return super().post(request, **kwargs)

class DiscountAndTypeUpdateView(UpdateView):
    model = PosOrder
    form_class = DiscountAndTypeForm

    def form_valid(self, form):
        self.object = form.save()
        context = prepare_order_context(self.request)
        return render(self.request, stanndard_order_update_calculations_template, context)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            'form': form,
            'field_name': 'discount_and_type'
        })
