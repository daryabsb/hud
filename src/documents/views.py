from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from src.documents.models import Document
import django_tables2 as tables


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
    return render(request, "documents/list.html", {"table": table})



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