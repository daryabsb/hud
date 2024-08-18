from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from src.documents.models import Document
import django_tables2 as tables
from src.documents.filters import DocumentFilter

class DocumentTable(tables.Table):
    class Meta:
        model = Document
        template_name = "django_tables2/bootstrap5-responsive.html"  # You can use a different template if preferred
        fields = (
            "number", "user", "customer", "cash_register", "order",
            "document_type", "warehouse", "date", "reference_document_number",
            "internal_note", "note", "due_date", "discount", "discount_type",
            "discount_apply_rule", "paid_status", "stock_date", "total", "is_clocked_out",
            "created", "updated"
        )

from django.shortcuts import render
import django_tables2 as tables
# from .tables import DocumentTable

def document_list_view(request):
    table = DocumentTable(Document.objects.all())
    tables.RequestConfig(
        request, 
        paginate={"per_page": 10}).configure(table)
    return render(request, "documents/list-view.html", {"table": table})


def document_list(request):
    filter = DocumentFilter

    return render(request, "documents/list.html", {"filter": filter})

['FILTER_DEFAULTS', 'Meta', 
  'base_filters', 'declared_filters', 'errors', 'filter_by_ref', 'filter_for_field', 'filter_for_lookup', 
  'filter_queryset', 'form', 'get_fields', 'get_filter_name', 'get_filters', 'get_form_class', 
  'handle_unrecognized_field', 'is_valid', 'qs'
  ]

from datatableview.views import DatatableView

class DocumentJsonView(DatatableView):
    model = Document
    json = True
    columns = [
        'id',  # Important for tracking row selections
        'number',
        'user__username',
        'customer__name',
        'cash_register__name',
        'order__id',
        'document_type__name',
        'warehouse__name',
        'date',
        'total',
        'paid_status',
    ]