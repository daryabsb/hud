from decimal import Decimal
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from src.documents.models import DocumentCategory, DocumentType
from src.documents.forms import DocumentFilterForm
from src.documents.forms import DocumentCreateForm, AddDocumentItem
from src.products.models import Product, ProductGroup
from src.stock.models import StockControl
from src.stock.forms import StockControlForm
from src.accounts.forms import CustomerForm
from src.orders.forms import DocumentForm
from src.orders.models import PosOrderItem

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
    from src.orders.forms import CreateSaleForm
    from django.forms import model_to_dict
    from src.orders.models import PosOrder

    # form = CreateSaleForm
    # form = DocumentForm

    document_type = DocumentType.objects.first()

    groups = ProductGroup.objects.all()
    products = Product.objects.all()

    # dt_id = request.GET.get("dt-id", None)
    dt_id = request.GET.get("document-type", None)

    if dt_id:
        document_type = get_object_or_404(DocumentType, id=dt_id)
        # if document_type.stock_direction == 2:
        #     form = DocumentForm(
        #         initial={'document_type': document_type, 'user': request.user})
        # else:
        #     form = DocumentCreateForm(
        #         stock_direction=document_type.stock_direction)

    form = DocumentForm(
        initial={'document_type': document_type, 'user': request.user})

    orders = PosOrder.objects.filter(is_active=True)

    context = {
        "form": form,
        "groups": groups,
        "products": products,
        "items": range(9),
        "document_type": document_type,
        "orders": orders,

    }
    return render(request, 'mgt/documents/add/new/document.html', context)


def add_new_document_product_details(request, product_id):
    stock_control = None
    customer = None
    product = None
    decimal_init = Decimal(1)

    document_type_id = request.GET.get("document_type", None)
    order_number = request.GET.get("order-number", None)

    print('order = ', order_number)

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
        "order_number": order_number,
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


@login_required
@require_GET
def modal_delete_order_item(request, item_number):

    if item_number:
        item = get_object_or_404(PosOrderItem, number=item_number)
    
        context = {"item": item}
        return render(request, 'mgt/modals/confirm-delete-order-item.html', context)