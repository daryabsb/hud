from django.shortcuts import render, get_object_or_404
from django.views import View
from src.orders.models import PosOrder
from src.pos.forms import PosOrderForm

class GenericOrderModalView(View):
    """
    Modal view for the generic order update form.
    This view renders the modal template with the appropriate context.
    """
    template_name = 'cotton/pos/modals/generic_order_modal.html'
    
    def get(self, request, number):
        # Get the active order
        active_order = get_object_or_404(PosOrder, number=number)
        
        # Get the fields to include from query parameters
        fields_param = request.GET.get('fields')
        form_fields = None
        
        if fields_param:
            from src.pos.const import POS_FORM_FIELDS
            # Split the comma-separated list of fields
            form_fields = [field.strip() for field in fields_param.split(',') 
                          if field.strip() in POS_FORM_FIELDS]
        
        # Create a form with the specified fields
        if form_fields:
            form_class = type(
                f"Partial{PosOrderForm.__name__}", 
                (PosOrderForm,), 
                {'Meta': type('Meta', (PosOrderForm.Meta,), 
                           {'fields': form_fields})}
            )
            form = form_class(instance=active_order)
        else:
            # Default to showing status and note fields
            form_class = type(
                f"Partial{PosOrderForm.__name__}", 
                (PosOrderForm,), 
                {'Meta': type('Meta', (PosOrderForm.Meta,), 
                           {'fields': ['status', 'note']})}
            )
            form = form_class(instance=active_order)
        
        # Prepare the context
        context = {
            'active_order': active_order,
            'form': form,
        }
        
        return render(request, self.template_name, context)