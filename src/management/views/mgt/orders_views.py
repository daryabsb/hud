
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from src.documents.forms import DocumentCreateForm
from src.documents.models import DocumentType
from src.products.models import Product, ProductGroup
from src.documents.models import Document
from src.management.filters import DocumentFilterForm as DocumentFilter
from src.management.views import DocumentSerializer


'''
cases:

PURCHASE = supplier, items, dates (due, stock), external document, paid_status 
SALE = customer, items, dates (due, stock), external document, paid_status 
'''

@login_required
def mgt_orders(request):
    filter = DocumentFilter(request.GET, queryset=Document.objects.all())
    form = DocumentFilter.form
    documents = Document.objects.all()

    documents_dict = DocumentSerializer(documents, many=True)

    context = {
        'filter': filter,
        'form': form,
        'documents_dict': documents_dict,
    }
    return render(request, 'mgt/orders/list.html', context)


def add_new_document_tab(request):
    ''' dt_id = document_type_id '''
    form = DocumentCreateForm
    groups = ProductGroup.objects.all()
    products = Product.objects.all()

    # dt_id = request.GET.get("dt-id", None)
    dt_id = request.GET.get("document-type", None)

    if dt_id:
        document_type = get_object_or_404(DocumentType, id=dt_id)

    context = {
        "form": form,
        "groups": groups,
        "products": products,
        "items": range(9),
        "document_type": document_type

    }
    return render(request, 'mgt/documents/renders/add-new-document.html', context)
