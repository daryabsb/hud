from collections import defaultdict

from django.urls import reverse
from src.management.utils import generate_barcode
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from src.products.models import Product, ProductGroup, ProductComment, Barcode
from src.tax.models import ProductTax, Tax
from src.stock.models import StockControl
from django.forms import modelformset_factory
from src.products.forms import (
    ProductGroupForm, ConfirmPasswordForm, ProductDetailsForm,
    BarcodeForm, ProductCommentForm
)
from src.stock.forms import StockControlForm
from src.tax.forms import ProductTaxForm
from src.accounts.forms import CustomerForm

from src.accounts.models import User, Customer
# Create your views here.
from django.db.models import Q
from django.contrib.auth.models import Group, Permission


def mgt_products(request, slug=None):
    products = Product.objects.all()
    groups = ProductGroup.objects.all()

    if slug:
        # if slug != 'products':
        group = ProductGroup.objects.filter(slug=slug).first()
        products = products.filter(
            Q(parent_group=group) | Q(parent_group__parent=group))

    # Pagination logic
    page_size = request.GET.get('page-size', 8)
    page_size = int(page_size)

    paginator = Paginator(products, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine pagination range
    num_pages = paginator.num_pages
    print("page_obj.count = ", page_obj.end_index() - page_obj.start_index() + 1)
    current_page = page_obj.number
    if num_pages <= 5:
        page_range = range(1, num_pages + 1)
    else:
        start = max(1, current_page - 2)
        end = min(num_pages, current_page + 2)
        if start == 1:
            end = min(5, num_pages)
        if end == num_pages:
            start = max(1, num_pages - 4)
        page_range = range(start, end + 1)

    # Range of page sizes for the select dropdown
    page_size_range = range(6, 11)
    context = {
        "products": page_obj,
        "products_count": products.count(),
        "page_range": page_range,
        "page_size": page_size,
        "page_size_range": page_size_range,
        "groups": groups,
    }

    if request.htmx:
        return render(request, 'mgt/products/renders/update-products.html', context)

    if not page_obj:
        return HttpResponseRedirect('/mgt/products/products/')

    return render(request, 'mgt/products/list.html', context)


def add_product(request, product_id=None):
    from django.utils.text import slugify
    product = None
    product_tax_queryset = ProductTax.objects.none()
    barcode = None
    stock_control = None
    product_comment_queryset = None
    customer = None

    if product_id:
        product = get_object_or_404(Product, id=product_id)
        barcode = Barcode.objects.filter(product=product).first()
        product_tax_queryset = ProductTax.objects.filter(product=product)
        stock_control = StockControl.objects.filter(product=product).first()
        customer = stock_control.customer if stock_control else None
        product_comment_queryset = ProductComment.objects.filter(
            product=product)

    if request.method == 'POST':
        product_form = ProductDetailsForm(request.POST, request.FILES, instance=product)
        barcode_form = BarcodeForm(request.POST, instance=barcode)
        product_tax_formset = modelformset_factory(ProductTax, form=ProductTaxForm, extra=1)(
            request.POST, queryset=product_tax_queryset)
        stock_control_form = StockControlForm(request.POST)
        customer_form = CustomerForm(request.POST, instance=customer)
        product_comment_formset = modelformset_factory(ProductComment, form=ProductCommentForm, extra=1)(
            request.POST, queryset=product_comment_queryset)
        tax_ids = request.POST.getlist('tax')

        if product_form.is_valid():
            product = product_form.save(commit=False)
            if not product_id:  # Only set user and initial slug if it's a new product
                product.user = request.user
                product.slug = slugify(product.name)
            else:  # For existing product, update slug only if name has changed
                if product_form.cleaned_data['name'] != product.name:
                    product.slug = slugify(product_form.cleaned_data['name'])
            product.save()
        else:
            print("Product form is not valid")

        if barcode_form.is_valid():
            barcode = barcode_form.save(commit=False)
            barcode.product = product
            barcode.user = request.user

            if not barcode_form.cleaned_data['value']:  # Check if the barcode is not provided
                barcode.value = generate_barcode()
            barcode.save()
        else:
            print("Barcode is not valid")

        if product_tax_formset.is_valid():
            for form in product_tax_formset:
                if form.cleaned_data:  # Only save the form if it's not empty
                    product_tax = form.save(commit=False)
                    product_tax.user = request.user
                    product_tax.product = product
                    product_tax.save()
        else:
            print("ProductTax formset is not valid")

        # if tax_ids:
        #     for id in tax_ids:
        #         tax = Tax.objects.get(id=id)
        #         if not tax.is_tax_on_total:
        #             ProductTax.objects.create(
        #                 user=request.user,
        #                 tax=tax,
        #                 product=product
        #             )

        if stock_control_form.is_valid():
            stock_control = stock_control_form.save(commit=False)
            stock_control.user = request.user
            stock_control.product = product
            stock_control.save()

        if product_comment_formset.is_valid():
            for form in product_comment_formset:
                comment = form.save(commit=False)
                comment.user = request.user
                comment.product = product
                comment.save()
            

        # Replace 'product_list' with your product list view name
        return redirect(reverse('mgt:products'))

    else:
        product_form = ProductDetailsForm()
        barcode_form = BarcodeForm()
        product_tax_formset = modelformset_factory(
            ProductTax, form=ProductTaxForm, extra=1)(queryset=ProductTax.objects.none())
        stock_control_form = StockControlForm()
        customer_form = CustomerForm()
        product_comment_formset = modelformset_factory(
            ProductComment, form=ProductCommentForm, extra=1)(queryset=ProductComment.objects.none())

    return render(request, 'mgt/products/list.html', {
        'groups': ProductGroup.objects.all(),
        'product': product,
        'product_form': product_form,
        'barcode_form': barcode_form,
        'product_tax_formset': product_tax_formset,
        'stock_control_form': stock_control_form,
        'customer_form': customer_form,
        'product_comment_formset': product_comment_formset,
    })
