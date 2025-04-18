from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.accounts.models import User
from src.products.forms import ProductGroupForm, ConfirmPasswordForm
from src.products.models import Product, ProductGroup, ProductComment, Barcode
from django.forms import modelformset_factory, formset_factory
from src.products.forms import (
    ProductGroupForm, ConfirmPasswordForm, ProductDetailsForm,
    BarcodeForm, ProductCommentForm
)
from src.documents.models import DocumentCategory, DocumentType
from src.documents.forms import DocumentCreateForm
from src.printers.forms import ProductPrintStationForm
from src.stock.forms import StockControlForm
from src.stock.models import StockControl
from src.tax.forms import ProductTaxForm
from src.accounts.forms import CustomerForm
from src.tax.models import ProductTax, Tax
from decimal import Decimal


@login_required
@require_GET
def modal_add_group(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'mgt/modals/add-group-modal.html', context)


@login_required
@require_GET
def modal_add_user(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'mgt/modals/add-user-modal.html', context)


def add_doc_filter_products(request):
    keywords = request.GET.get('add-doc-product-filter', None)
    qs = Product.objects.filter(is_enabled=True)
    document_type = None

    dt_id = request.GET.get("document-type", None)

    if dt_id:
        document_type = get_object_or_404(DocumentType, id=dt_id)

    if keywords:
        qs = qs.filter(name__icontains=keywords)
        # qs = qs.filter(
        #         # **filter_dict
        #         Q(customer=customer)
        #         | Q(document_type__id=int(col_search_value))
        #         | Q(id=col_search_value)
        #         | Q(paid_status=bool(col_search_value))
        #     )
    print('document_type = ', document_type)
    context = {
        "products": qs,
        "document_type": document_type
    }

    return render(request, 'mgt/documents/renders/add-document-products.html', context)
