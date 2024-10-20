from django.shortcuts import get_object_or_404, render
from src.documents.forms import DocumentCreateForm
from src.documents.models import DocumentType
from src.products.models import Product, ProductGroup

'''
cases:

PURCHASE = supplier, items, dates (due, stock), external document, paid_status 
SALE = customer, items, dates (due, stock), external document, paid_status 
'''


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
