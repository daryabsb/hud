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
from src.printers.forms import ProductPrintStationForm
from src.stock.forms import StockControlForm
from src.stock.models import StockControl
from src.tax.forms import ProductTaxForm
from src.accounts.forms import CustomerForm
from src.tax.models import ProductTax, Tax


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


@login_required
@require_GET
def modal_add_product(request):
    max_forms = Tax.objects.filter(is_tax_on_total=False).count()
    users = User.objects.all()
    product = None
    product_tax_queryset = ProductTax.objects.none()
    barcode = None
    stock_control = None
    product_comment_queryset = None
    customer = None
    product_group = request.GET.get('group-id', None)
    product_id = request.GET.get('product-id', None)

    if product_id:
        product = get_object_or_404(Product, id=product_id)
        barcode = Barcode.objects.filter(product=product).first()
        product_tax_queryset = ProductTax.objects.filter(product=product)
        stock_control = StockControl.objects.filter(product=product).first()
        customer = stock_control.customer if stock_control else None
        product_comment_queryset = ProductComment.objects.filter(
            product=product)
        product_group = product.parent_group
    product_form = ProductDetailsForm(instance=product, initial={
                                      'parent_group': product_group})
    barcode_form = BarcodeForm(instance=barcode)
    product_printstation_form = ProductPrintStationForm()

    product_tax_form = ProductTaxForm(initial={'tax': Tax.objects.first()})
    stock_control_form = StockControlForm(instance=stock_control)
    customer_form = CustomerForm(instance=customer)
    product_comment_formset = modelformset_factory(
        ProductComment, form=ProductCommentForm, extra=0)
    # (queryset=product_comment_queryset)

    for tax in product_tax_queryset:
        print(tax.product.name, ' : ', tax)

    product_tax_formset = modelformset_factory(
        ProductTax, form=ProductTaxForm, max_num=max_forms, extra=0)(
            queryset=product_tax_queryset
    )

    context = {
        "users": users,
        'product': product,
        'product_form': product_form,
        'barcode_form': barcode_form,
        'max_forms': max_forms,
        'product_tax_formset': product_tax_formset,
        'product_tax_form': product_tax_form,
        'stock_control_form': stock_control_form,
        'product_printstation_form': product_printstation_form,
        'customer_form': customer_form,
        'product_comment_formset': product_comment_formset,
    }
    return render(request, 'mgt/modals/add-product-modal.html', context)


def add_to_product_tax_formset(request):
    template = 'mgt/tabs/add-product/side-forms/product-tax-formset.html'
    max_forms = Tax.objects.filter(is_tax_on_total=False).count()
    product_id = request.GET.get('product-id', None)
    product = None
    product_tax_queryset = ProductTax.objects.none()
    print('check if product id? ', product_id)
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        product_tax_queryset = ProductTax.objects.filter(product=product)

    product_tax_formset = modelformset_factory(
        ProductTax, form=ProductTaxForm, max_num=max_forms, extra=1)(
            queryset=product_tax_queryset
    )

    context = {
        'product': product,
        'product_tax_formset': product_tax_formset,
        'max_forms': max_forms,
    }
    return render(request, template, context)


def delete_product_tax(request):
    template = 'mgt/tabs/add-product/side-forms/product-tax-formset.html'
    max_forms = Tax.objects.filter(is_tax_on_total=False).count()
    product_id = request.POST.get('product-id', None)
    product = None
    product_tax_queryset = ProductTax.objects.none()

    product_tax_id = request.POST.get('product_tax_id')

    if product_id and product_tax_id:
        product_tax = get_object_or_404(ProductTax, id=product_tax_id).delete()
        product = get_object_or_404(Product, id=product_id)
        product_tax_queryset = ProductTax.objects.filter(product=product)

    ProductTaxFormset = modelformset_factory(
        ProductTax, form=ProductTaxForm, max_num=max_forms, extra=0)
    product_tax_formset = ProductTaxFormset(queryset=product_tax_queryset)

    context = {
        'product': product,
        'product_tax_formset': product_tax_formset,
        'max_forms': max_forms,
    }
    return render(request, template, context)


@login_required
@require_GET
def modal_delete_product(request):
    product_id = request.GET.get('product-id', None)
    product = get_object_or_404(Product, id=product_id)
    print("product_delete = ", product.name)
    form = ConfirmPasswordForm()
    context = {"product": product, "form": form}
    return render(request, 'mgt/modals/confirm-delete-product.html', context)


@login_required
@require_GET
def modal_update_product_group(request):
    group = None
    group_id = request.GET.get('group-id', None)
    parent_id = request.POST.get('parent-id', None)

    if group_id:
        group = get_object_or_404(ProductGroup, id=group_id)
        form = ProductGroupForm(instance=group)
        context = {"group": group, "form": form}
        return render(request, 'mgt/modals/add-product-group-modal.html', context)
    if parent_id:
        parent_group = get_object_or_404(ProductGroup, id=parent_id)
        form = ProductGroupForm(initial={'parent_group': parent_group})
    else:
        form = ProductGroupForm()
    return render(request, 'mgt/modals/add-product-group-modal.html', {"form": form})


@login_required
@require_GET
def modal_add_product_group(request):

    parent_id = request.GET.get('group-id', None)

    if parent_id:
        parent = get_object_or_404(ProductGroup, id=parent_id)
    else:
        parent = get_object_or_404(ProductGroup, slug='products')

    form = ProductGroupForm(initial={'parent': parent})
    return render(request, 'mgt/modals/add-product-group-modal.html', {"form": form})


@login_required
@require_GET
def modal_delete_product_group(request):
    group_id = request.GET.get('group-id', None)
    group = get_object_or_404(ProductGroup, id=group_id)
    print("group_delete = ", group.name)
    form = ConfirmPasswordForm()
    context = {"group": group, "form": form}
    return render(request, 'mgt/modals/confirm-delete-group.html', context)


def show_customer_form(request):
    customer_form = CustomerForm()
    context = {"customer_form": customer_form}
    return render(
        request, 'mgt/tabs/add-product/side-forms/customer-form.html', context)


def append_product_tax_form(request):
    tax_ids = request.GET.getlist('tax-id', None)
    tax_ids = request.GET.getlist('tax', None)
    is_first_set = ''

    if tax_ids:
        tax = Tax.objects.exclude(id__in=tax_ids).first()
    else:
        tax = Tax.objects.first()
        is_first_set = 'is-first-set'

    if not tax or tax.id in tax_ids:
        is_first_set = ''
        return render(
            request,
            'mgt/tabs/add-product/side-forms/max-reached.html', {'is_first_set': is_first_set})

    product_tax_form = ProductTaxForm(initial={'tax': tax})
    context = {
        'tax': tax,
        'product_tax_form': product_tax_form,
        'is_first_set': is_first_set,
    }
    return render(
        request,
        'mgt/tabs/add-product/side-forms/product-tax-form.html', context)


def generate_barcode_for_product(request):
    from src.management.utils import generate_barcode
    from src.products.forms import BarcodeForm
    template = 'mgt/tabs/add-product/side-forms/barcode-field.html'
    barcode = generate_barcode()
    barcode_form = BarcodeForm(initial={"value": barcode})
    context = {"barcode_form": barcode_form}
    return render(request, template, context)


def select_product_fields_to_export(request):
    target = request.GET.get('target', 'csv')
    product_ids = request.GET.getlist('product-row', None)
    fields = [field for field in Product._meta.get_fields()]
    product_row = [field.name for field in fields if not (
        field.many_to_many or field.one_to_many)]
    context = {
        'fields': product_row,
        'target': target,
        'product_ids': product_ids
    }
    return render(request, 'mgt/modals/select-product-fields.html', context)
