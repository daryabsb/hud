from decimal import Decimal

from django.shortcuts import get_object_or_404, render
from src.documents.models import DocumentCategory, DocumentType
from src.documents.forms import DocumentFilterForm
from src.documents.forms import DocumentCreateForm
from src.products.models import Product, ProductGroup
from src.stock.models import StockControl
from src.stock.forms import StockControlForm
from src.accounts.forms import CustomerForm


def modal_add_document(request):
    from src.documents.forms import DocumentFilterForm

    categories = DocumentCategory.objects.all()
    selected_cat = categories.first()
    document_types = DocumentType.objects.filter(category=selected_cat)

    form = DocumentFilterForm()

    context = {
        "form": form,
        "selected_cat": selected_cat,
        "categories": categories,
        "first_type": document_types.first(),
        "document_types": document_types,
    }
    return render(request, 'mgt/modals/add-document-modal.html', context)


def modal_select_document_type(request):

    categories = DocumentCategory.objects.all()
    selected_cat = categories.first()
    document_types = DocumentType.objects.filter(category=selected_cat)

    form = DocumentFilterForm()

    context = {
        "form": form,
        "selected_cat": selected_cat,
        "categories": categories,
        "first_type": document_types.first(),
        "document_types": document_types,
    }
    return render(request, 'mgt/modals/select-document-type-modal.html', context)


def add_new_document_tab(request):
    ''' dt_id = document_type_id '''
    form = DocumentCreateForm
    groups = ProductGroup.objects.all()
    products = Product.objects.all()

    # dt_id = request.GET.get("dt-id", None)
    dt_id = request.GET.get("document-type", None)

    if dt_id:
        document_type = get_object_or_404(DocumentType, id=dt_id)
        form = DocumentCreateForm(
            stock_direction=document_type.stock_direction)

    context = {
        "form": form,
        "groups": groups,
        "products": products,
        "items": range(9),
        "document_type": document_type

    }
    return render(request, 'mgt/documents/renders/add-new-document.html', context)


def add_new_document_product_details(request, product_id):
    from src.documents.forms import DocumentCreateForm, AddDocumentItem
    stock_control = None
    customer = None
    product = None
    decimal_init = Decimal(1)

    document_type_id = request.GET.get("document_type", None)

    if document_type_id:
        document_type = get_object_or_404(DocumentType, id=document_type_id)

    if product_id:
        product = get_object_or_404(Product, id=product_id)
        stock_control = StockControl.objects.filter(product=product).first()
        customer = stock_control.customer if stock_control else None

    stock_direction = document_type.stock_direction

    if stock_direction == 1:
        pass
    elif stock_direction == 2:
        pass
    else:
        pass

    document_item_form = AddDocumentItem(
        stock_direction=document_type.stock_direction, product=product,
        initial={
            'product': product.id,
            'quantity': 1,
            'price_before_tax': product.price,
            'price': decimal_init * product.price,
            'discount': 0,
            'total_before_tax': decimal_init * product.price,
            'total': decimal_init * product.price
        }
    )

    stock_control_form = StockControlForm(instance=stock_control)
    customer_form = CustomerForm(instance=customer)

    context = {
        "stock_control_form": stock_control_form,
        "customer_form": customer_form,
        "document_type": document_type,
        "form": document_item_form,
        "product": product,
    }

    return render(request, 'mgt/modals/add-document-product-modal.html', context)


def filter_document_type(request):

    category_id = request.GET.get("category-id", None)

    categories = DocumentCategory.objects.all()

    if category_id:
        cat = categories.get(id=int(category_id))
    else:
        cat = categories.first()

    document_types = DocumentType.objects.filter(category=cat)

    context = {
        "document_types": document_types,
        "first_type": document_types.first()
    }
    return render(request, 'mgt/forms/document_type_select.html', context)

