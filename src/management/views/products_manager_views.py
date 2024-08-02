import ast
import openpyxl
from django.http import HttpResponse
import os
import csv
from django.conf import settings
from html2image import Html2Image  # Or imgkit
from django.template.loader import render_to_string
from django.urls import reverse
from src.management.utils import generate_barcode
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from src.products.models import Product, ProductGroup, ProductComment, Barcode
from src.tax.models import ProductTax, Tax
from src.stock.models import StockControl
from src.management.const import PRODUCTS_DESIRED_ORDER, generate_filename
from django.forms import modelformset_factory
from src.products.forms import (
    ProductGroupForm, ConfirmPasswordForm, ProductDetailsForm,
    BarcodeForm, ProductCommentForm, PriceTagForm
)
import after_response
from src.stock.forms import StockControlForm
from src.tax.forms import ProductTaxForm
from src.accounts.forms import CustomerForm

from src.accounts.models import User, Customer
# Create your views here.
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from src.configurations.models import ApplicationProperty
from src.configurations.forms import ApplicationPropertyForm
from src.core.utils import convert_value
from django.forms import modelformset_factory
from django.db.models import Q, F
from src.core.utils import get_fields
from django.http import JsonResponse


def product_datatable_view(request):
    draw = int(request.GET.get("draw", "1"))
    length = int(request.GET.get("length", "10"))
    start = int(request.GET.get("start", "0"))
    search_value = request.GET.get("search[value]", None)

    qs = Product.objects.select_related('currency', 'barcode').annotate(
        user__name=F('user__name'),
        barcode__value=F('barcode__value'),
        parent_group__name=F('parent_group__name'),
        currency__name=F('currency__name'),
        # image_url=F('image__url'),
    ).order_by("id")

    if search_value:
        qs = qs.filter(
            Q(name__icontains=search_value)
            | Q(code__icontains=search_value)
            | Q(description__icontains=search_value)
        )

    filtered_count = qs.count()
    qs = qs[start: start + length]

    data = list(qs.values(*get_fields('products')))

    return JsonResponse({
        "recordsTotal": Product.objects.count(),
        "recordsFiltered": filtered_count,
        "draw": draw,
        "data": data,
    }, safe=False)


def mgt_products(request, slug=None):
    groups = ProductGroup.objects.all()

    products = Product.objects.all()
    fields = [field for field in Product._meta.get_fields()]
    product_row = [field.name for field in fields if not (
        field.many_to_many or field.one_to_many)]
    all_products = products
    if slug:
        # if slug != 'products':
        group = ProductGroup.objects.filter(slug=slug).first()
        products = all_products.filter(
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

    print('This view is called')

    # Range of page sizes for the select dropdown
    page_size_range = range(6, 11)
    context = {
        "products": page_obj,
        "all_products": all_products,
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
        product_form = ProductDetailsForm(
            request.POST or None, request.FILES, instance=product)
        barcode_form = BarcodeForm(request.POST or None, instance=barcode)

        ProductTaxFormset = modelformset_factory(
            ProductTax, form=ProductTaxForm, extra=1)
        product_tax_formset = ProductTaxFormset(
            request.POST or None, queryset=product_tax_queryset)

        stock_control_form = StockControlForm(request.POST)
        customer_form = CustomerForm(request.POST or None, instance=customer)
        ProductCommentFormset = modelformset_factory(
            ProductComment, form=ProductCommentForm, extra=1)
        product_comment_formset = ProductCommentFormset(
            request.POST or None, queryset=product_comment_queryset)
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

            # Check if the barcode is not provided
            if not barcode_form.cleaned_data['value']:
                barcode.value = generate_barcode()
            barcode.save()
        else:
            print("Barcode is not valid")

        if product_tax_formset.is_valid():
            for form in product_tax_formset:
                if form.instance and form.instance.id:
                    form.save()
                else:
                    if form.is_valid():
                        product_tax = form.save(commit=False)
                        product_tax.user = request.user
                        product_tax.product = product
                        product_tax.save()
                    else:
                        print(form.errors)  # Print individual form errors
        else:
            print("ProductTax formset is not valid")
            print(product_tax_formset.errors)  # Print formset errors

        if stock_control_form.is_valid():
            stock_control = stock_control_form.save(commit=False)
            stock_control.user = request.user
            stock_control.product = product
            stock_control.save()

        if product and product.parent_group.slug:
            parent_slug = product.parent_group.slug
        else:
            parent_slug = 'products'

        return redirect(reverse('mgt:filter-products', kwargs={'slug': parent_slug}))


def delete_product(request):
    from django.contrib.auth import authenticate
    product_id = request.POST.get('product-id', None)
    form = ConfirmPasswordForm(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user is not None:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            products = Product.objects.all()
            context = {
                "products": products,
            }
            return render(request, 'mgt/products/partials/products-table.html', context)


def mgt_invoice_template_view(request):
    return render(request, 'mgt/products/invoice-template.html', {})


def mgt_price_tags3(request):
    products = Product.objects.all()
    groups = ProductGroup.objects.all()
    return render(request, 'mgt/products/price-tags.html', {"products": products, "groups": groups})


def render_price_tag(product, options={}, is_preview=False):
    '''
    predicted numbers:

    '''

    if is_preview:
        for key, value in options.items():
            if type(value) == int:
                options[key] = options[key] * 3
    return render_to_string('mgt/products/price-tags/partials/price_tag.html', {
        'product': product,
        'is_preview': is_preview,
        **options
    })


def prepare_price_tag_forms(queryset):
    queryset = ApplicationProperty.objects.filter(
        section__name='price_tags')
    option_forms = {}

    for setting in queryset:
        options_dict = {}
        form = ApplicationPropertyForm(instance=setting)

        options_dict["form"] = form
        options_dict["name"] = setting.name
        options_dict["id"] = setting.id
        options_dict["value"] = convert_value(setting.value)
        options_dict["title"] = setting.title
        options_dict["description"] = setting.description
        options_dict["input_type"] = setting.input_type
        options_dict["editable"] = setting.editable
        options_dict["order"] = setting.order
        options_dict["params"] = setting.params
        options_dict["created"] = setting.created
        options_dict["updated"] = setting.updated

        option_forms[setting.name] = options_dict

    return option_forms


def mgt_price_tags_control(request):
    product_ids = request.GET.getlist('product_ids')

    options_queryset = ApplicationProperty.objects.filter(
        section__name='price_tags')
    options = {item['name']: convert_value(item['value'])
               for item in options_queryset.values('name', 'value')}

    option_forms = prepare_price_tag_forms(options_queryset)

    if product_ids:
        # If product_ids are provided, generate tags only for those products
        products = Product.objects.prefetch_related(
            'barcode').filter(id__in=product_ids)
        remaining_products = []
    else:
        # Otherwise, get the first 6 products and the rest for background generation
        all_products = Product.objects.prefetch_related('barcode').all()
        products = all_products[:6]
        remaining_products = all_products[6:]
    groups = ProductGroup.objects.all()
    tags = []

    for product in products:
        tag = {
            "product": product,
            "html": render_price_tag(product, options),
            **options
        }
        tags.append(tag)
    first_product = all_products.first()
    main_tag = {
        "product": first_product,
        "html": render_price_tag(first_product, options, is_preview=True)
    }

    form = PriceTagForm()

    context = {'tags': tags, 'main_tag': main_tag, 'products': products,
               'groups': groups, 'option_forms': option_forms}
    return render(request, 'mgt/products/price-tags/price-tag-control.html', context)


def mgt_price_tags_preview(request):

    options_queryset = ApplicationProperty.objects.filter(
        section__name='price_tags')

    options_dict = {}
    for option in options_queryset:
        option_value = request.GET.get(option.name, None)
        if option_value:
            # if option_value == 'on'
            options_dict[option.name] = convert_value(option_value)
    template = 'mgt/products/price-tags/partials/main-tag.html'

    product = Product.objects.first()

    main_tag = {
        "product": product,
        "html": render_price_tag(product, options_dict, is_preview=True)
    }
    return render(request, template, {'main_tag': main_tag})


def mgt_price_tags_set_default(request):

    options_queryset = ApplicationProperty.objects.filter(
        section__name='price_tags')

    options_dict = {}
    for option in options_queryset:
        option_value = request.GET.get(option.name, None)

        if option_value:
            # if option_value == 'on'
            option.value = convert_value(option_value)
            option.save(force_update=True)
            options_dict[option.name] = convert_value(option_value)
    template = 'mgt/products/price-tags/partials/main-tag.html'

    product = Product.objects.first()

    main_tag = {
        "product": product,
        "html": render_price_tag(product, options_dict, is_preview=True)
    }
    return render(request, template, {'main_tag': main_tag})


# TODO: add printing to the price tags
def mgt_price_tags_print_selected(request):
    selected_products = request.GET.getlist('price-tag-products', [])

    fields = [field for field in Product._meta.get_fields()]
    header_row = [field.name for field in fields if not (
        field.many_to_many or field.one_to_many)]

    print("header_row = ", header_row)

    if selected_products:
        for id in selected_products:
            product = get_object_or_404(Product, id=id)
            html = render_price_tag(product, options_dict, is_preview=True)
            print('product_html = ', html)

    return HttpResponse("The selected product printed successfully!")


fields = [
    'document_items', 'comments', 'order_items', 'product_print_stations', 'productTaxes',
    'stock_controls',
    'barcode', 'stocks',
    'id', 'user', 'name', 'slug', 'parent_group', 'code', 'description', 'plu', 'measurement_unit',
    'price', 'currency', 'is_tax_inclusive_price', 'is_price_change_allowed', 'is_service',
    'is_using_default_quantity', 'is_product', 'cost', 'margin', 'image',
    'color', 'is_enabled', 'age_restriction', 'last_purchase_price', 'rank', 'created', 'updated'
]
fields2 = [
    'barcode', 'id', 'user', 'name', 'slug', 'parent_group', 'code', 'description', 'plu', 'measurement_unit',
    'price', 'currency', 'is_tax_inclusive_price', 'is_price_change_allowed', 'is_service',
    'is_using_default_quantity', 'is_product', 'cost', 'margin', 'image', 'color',
    'is_enabled', 'age_restriction', 'last_purchase_price', 'rank', 'created', 'updated'
]


def mgt_export_products_to_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    product_ids = request.POST.get('product-ids', None)
    if product_ids:
        try:
            # Convert the string representation of the list to an actual list
            product_ids = ast.literal_eval(product_ids)
            # Convert list of string IDs to list of integers
            product_ids = [int(id) for id in product_ids]
        except (ValueError, SyntaxError):
            product_ids = []

        products = Product.objects.filter(id__in=product_ids)
    else:
        products = Product.objects.all()
    filename = generate_filename('Products', products.count())
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    # Get the selected fields from the POST request
    selected_fields = request.POST.getlist('selected-fields', [])

    # Sort selected fields based on the desired order
    selected_fields_sorted = sorted(
        selected_fields, key=lambda x: PRODUCTS_DESIRED_ORDER.index(x)
        if x in PRODUCTS_DESIRED_ORDER
        else len(PRODUCTS_DESIRED_ORDER)
    )

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the headers dynamically
    headers = [field.replace('_', ' ').capitalize()
               for field in selected_fields_sorted]
    writer.writerow(headers)

    # Fetch the products from the database

    # Write the product data dynamically
    for product in products:
        row = []
        for field in selected_fields_sorted:
            # Handle related fields and special cases
            if '__' in field:
                related_field_parts = field.split('__')
                value = product
                for part in related_field_parts:
                    value = getattr(value, part, '')
                    if not isinstance(value, (str, int, float, bool, type(None))):
                        value = str(value)
            else:
                value = getattr(product, field, '')
                # Handle special cases for non-string values
                if field == 'currency':
                    value = str(value)
                elif field == 'image':
                    value = value.url if value else ''
                elif field in ['created', 'updated']:
                    value = value.strftime('%Y %m %d - %I:%M:%S %p')
                elif not isinstance(value, (str, int, float, bool, type(None))):
                    value = str(value)
            row.append(value)
        writer.writerow(row)

    return response


def mgt_export_products_to_excel(request):
    # Create an in-memory workbook and worksheet
    product_ids = request.POST.get('product-ids', None)
    if product_ids:
        try:
            # Convert the string representation of the list to an actual list
            product_ids = ast.literal_eval(product_ids)
            # Convert list of string IDs to list of integers
            product_ids = [int(id) for id in product_ids]
        except (ValueError, SyntaxError):
            product_ids = []

        products = Product.objects.filter(id__in=product_ids)
    else:
        products = Product.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Products'

    # Get the selected fields from the POST request
    selected_fields = request.POST.getlist('selected-fields', [])

    # Sort selected fields based on the desired order
    selected_fields_sorted = sorted(
        selected_fields, key=lambda x: PRODUCTS_DESIRED_ORDER.index(x)
        if x in PRODUCTS_DESIRED_ORDER
        else len(PRODUCTS_DESIRED_ORDER)
    )

    # Write the headers dynamically
    headers = [field.replace('_', ' ').capitalize()
               for field in selected_fields_sorted]
    ws.append(headers)

    # Write the product data dynamically
    for product in products:
        row = []
        for field in selected_fields_sorted:
            # Handle related fields and special cases
            if '__' in field:
                related_field_parts = field.split('__')
                value = product
                for part in related_field_parts:
                    value = getattr(value, part, '')
                    if not isinstance(value, (str, int, float, bool, type(None))):
                        value = str(value)
            else:
                value = getattr(product, field, '')
                # Handle special cases for non-string values
                if field == 'currency':
                    value = str(value)
                elif field == 'image':
                    value = value.url if value else ''
                elif field in ['created', 'updated']:
                    value = value.strftime('%Y %m %d - %I:%M:%S %p')
                elif not isinstance(value, (str, int, float, bool, type(None))):
                    value = str(value)
            row.append(value)
        ws.append(row)
    filename = generate_filename('Products', products.count())
    # Create a response object with the appropriate Excel header
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

    # Save the workbook to the response
    wb.save(response)
    return response


@after_response.enable
def generate_price_tags(products):
    hti = Html2Image(size=(630, 440))

    # Ensure the price_tags directory exists
    price_tags_dir = os.path.join(settings.MEDIA_ROOT, 'price_tags')
    os.makedirs(price_tags_dir, exist_ok=True)
    hti.output_path = price_tags_dir

    for product in products:
        html_content = render_to_string('mgt/products/price-tags/partials/price_tag.html', {
            'product': product,
            'margin': '10px',
            'show_name': True,
            'show_price': True,
            'show_sku': True,
            'show_barcode': True,
            'name_color': 'black',
            'price_color': 'red',
            'sku_color': 'blue',
            'price_size': 24,
            'sku_size': 14,
            'barcode_height': 50,
        })
        filename = f'{product.id}_price_tag.png'
        hti.screenshot(html_str=html_content, save_as=filename)


def mgt_price_tags(request):
    product_ids = request.GET.getlist('product_ids')

    if product_ids:
        # If product_ids are provided, generate tags only for those products
        products = Product.objects.prefetch_related(
            'barcode').filter(id__in=product_ids)
        remaining_products = []
    else:
        # Otherwise, get the first 6 products and the rest for background generation
        all_products = Product.objects.prefetch_related('barcode').all()
        products = all_products[:6]
        remaining_products = all_products[6:]

    groups = ProductGroup.objects.all()
    images = []

    # Generate fresh tags for the selected products
    hti = Html2Image(size=(630, 440))
    price_tags_dir = os.path.join(settings.MEDIA_ROOT, 'price_tags')
    os.makedirs(price_tags_dir, exist_ok=True)
    hti.output_path = price_tags_dir

    for product in products:
        html_content = render_to_string('mgt/products/price-tags/partials/price_tag.html', {
            'product': product,
            'margin': '10px',
            'show_name': True,
            'show_price': True,
            'show_sku': True,
            'show_barcode': True,
            'name_color': 'black',
            'price_color': 'red',
            'sku_color': 'blue',
            'price_size': 72,
            'sku_size': 48,
            'barcode_height': 100,
        })
        filename = f'{product.id}_price_tag.png'
        hti.screenshot(html_str=html_content, save_as=filename)
        images.append(os.path.join(settings.MEDIA_URL, 'price_tags', filename))

    # Generate remaining price tags after response
    if remaining_products:
        generate_price_tags.after_response(remaining_products)

    context = {'images': images, 'products': products, 'groups': groups}
    return render(request, 'mgt/products/price-tags/panel.html', context)


def mgt_price_tags2(request, slug=None):
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
    return render(request, 'mgt/products/price-tags.html', context)


form_contains = [
    'Meta',
    '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
    '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__html__',
    '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    '__weakref__',
    '_bound_fields_cache', '_bound_items', '_clean_fields', '_clean_form', '_errors',
    '_get_validation_exclusions', '_meta', '_post_clean', '_save_m2m', '_update_errors',
    '_validate_unique', '_widget_data_value',

    'add_error', 'add_initial_prefix', 'add_prefix', 'as_div', 'as_p', 'as_table', 'as_ul',
    'auto_id', 'base_fields', 'changed_data', 'clean', 'data', 'declared_fields', 'default_renderer',
    'empty_permitted', 'error_class', 'errors', 'field_order', 'fields', 'files', 'full_clean', 'get_context',
    'get_initial_for_field', 'has_changed', 'has_error', 'hidden_fields', 'initial', 'instance', 'is_bound',
    'is_multipart', 'is_valid', 'label_suffix', 'media', 'non_field_errors', 'order_fields', 'prefix',
    'render', 'renderer', 'save', 'template_name', 'template_name_div', 'template_name_label', 'template_name_p',
    'template_name_table', 'template_name_ul', 'use_required_attribute', 'validate_unique', 'visible_fields'
]
form_dir = [
    'Meta',
    '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
    '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__html__',
    '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    '__weakref__',

    '_bound_fields_cache', '_bound_items', '_clean_fields', '_clean_form', '_errors',
    '_get_validation_exclusions', '_meta', '_post_clean', '_save_m2m', '_update_errors',
    '_validate_unique', '_widget_data_value',

    'add_error', 'add_initial_prefix', 'add_prefix',
    'as_div', 'as_p', 'as_table', 'as_ul',
    'auto_id', 'base_fields', 'changed_data', 'clean', 'data', 'declared_fields',
    'default_renderer', 'empty_permitted', 'error_class', 'errors', 'field_order',
    'fields', 'files', 'full_clean', 'get_context', 'get_initial_for_field', 'has_changed',
    'has_error', 'hidden_fields', 'initial', 'instance', 'is_bound', 'is_multipart', 'is_valid',
    'label_suffix', 'media', 'non_field_errors', 'order_fields', 'prefix', 'render', 'renderer',
    'save', 'template_name', 'template_name_div', 'template_name_label', 'template_name_p',
    'template_name_table', 'template_name_ul', 'use_required_attribute', 'validate_unique',
    'visible_fields'
]

formset_dir = [
    '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
    '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__html__',
    '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__',
    '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
    '__subclasshook__', '__weakref__',

    '_construct_form', '_errors', '_existing_object', '_get_to_python', '_non_form_errors',
    '_should_delete_form',

    'absolute_max', 'add_fields', 'add_prefix',
    'as_div', 'as_p', 'as_table', 'as_ul',

    'auto_id', 'can_delete', 'can_delete_extra', 'can_order', 'clean', 'cleaned_data',
    'data', 'default_error_messages', 'delete_existing', 'deleted_forms', 'deletion_widget',
    'edit_only', 'empty_form', 'error_class', 'error_messages', 'errors', 'extra', 'extra_forms',
    'files', 'form', 'form_kwargs', 'form_renderer', 'forms', 'full_clean', 'get_context',
    'get_date_error_message', 'get_default_prefix', 'get_deletion_widget', 'get_form_error',
    'get_form_kwargs', 'get_ordering_widget', 'get_queryset', 'get_unique_error_message',
    'has_changed', 'initial', 'initial_extra', 'initial_form_count', 'initial_forms', 'is_bound',
    'is_multipart', 'is_valid', 'management_form', 'max_num', 'media', 'min_num', 'model',
    'non_form_errors', 'ordered_forms', 'ordering_widget', 'prefix', 'queryset', 'render',
    'renderer', 'save', 'save_existing', 'save_existing_objects', 'save_new', 'save_new_objects',
    'template_name', 'template_name_div', 'template_name_p', 'template_name_table', 'template_name_ul',
    'total_error_count', 'total_form_count', 'unique_fields', 'validate_max', 'validate_min', 'validate_unique'
]

reqpost = {'QueryDict': {
    'csrfmiddlewaretoken': ['RsRr1eQ908gPhlzthWOhb4eVmQCr06O6NPUZLiodNSTkj2G5ii8RkqNV6Yd20x9s'],
    'name': ['Organic Bananas'],
    'code': [''],
    'value': ['556828708663'],
    'measurement_unit': ['KG'],
    'parent_group': ['2'],
    'is_enabled': ['on'],
    'is_using_default_quantity': ['on'],
    'age_restriction': [''],
    'form-TOTAL_FORMS': ['2', '2'],
    'form-INITIAL_FORMS': ['1', '2'],
    'form-MIN_NUM_FORMS': ['0', '0'],
    'form-MAX_NUM_FORMS': ['2', '1000'],
    'form-0-tax': ['2'],
    'form-1-tax': ['3'],
    'product-id': ['1'],
    'cost': ['0.000'],
    'margin': ['100.000'],
    'price': ['1200.000'],
    'customer': ['1'],
    'reorder_point': ['0.0'],
    'preferred_quantity': ['1'],
    'is_low_stock_warning_enabled': ['on'],
    'low_stock_warning_quantity': ['1'],
    'form-0-comment': [''],
    'form-1-comment': [''],
    'color': ['#FFFFFF'],
    'image': ['']
}
}

post_data = {
    'QueryDict':
    {
        'csrfmiddlewaretoken': ['8xh0xs3BdSeMeJYxzNgRcR6pNqhkVVMw4UkyhwBF0CRhgq59A9ArldFpxySVVm7S'],
        'name': ['Organic Bananas'],
        'code': [''],
        'value': ['556828708663'],
        'measurement_unit': ['KG'],
        'parent_group': ['2'],
        'is_enabled': ['on'],
        'is_using_default_quantity': ['on'],
        'age_restriction': [''],

        'form-TOTAL_FORMS': ['2'],
        'form-INITIAL_FORMS': ['1'],
        'form-MIN_NUM_FORMS': ['0'],
        'form-MAX_NUM_FORMS': ['2'],
        'form-0-tax': ['3'],
        'form-1-tax': ['2'],
        'product-id': ['1'],
        'cost': ['0.000'],
        'margin': ['100.000'],
        'price': ['1200.000'],
        'customer': ['1'],
        'reorder_point': ['0.0'],
        'preferred_quantity': ['1'],
        'is_low_stock_warning_enabled': ['on'],
        'low_stock_warning_quantity': ['1'],
        'color': ['#FFFFFF'],
        'image': ['']
    }
}

barcode = [
    'DEFAULT_CHUNK_SIZE', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
    '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__',
    '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__',
    '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_committed', '_del_file',
    '_file', '_get_file', '_get_image_dimensions', '_require_file', '_set_file',

    'chunks', 'close', 'closed', 'delete', 'encoding', 'field', 'file', 'fileno', 'flush',
    'height', 'instance', 'isatty', 'multiple_chunks', 'name', 'newlines', 'open', 'path',
    'read', 'readable', 'readinto', 'readline', 'readlines', 'save', 'seek', 'seekable',
    'size', 'storage', 'tell', 'truncate', 'url', 'width', 'writable', 'write', 'writelines'
]


options = {
    'frame_padding': 8,
    'frame_width': 200,
    'frame_height': 125,
    'code_font_size': 10,
    'code_font_weight': 'bold',
    'code_font_color': '#000000',
    'code_margin_bottom': 3,
    'code_show': True,
    'name_font_size': 10,
    'name_font_weight': 'bold',
    'name_font_color': '#303030',
    'name_margin_bottom': 3,
    'name_show': False,
    'price_font_size': 15,
    'price_font_weight': 'bold',
    'price_font_color': '#000000',
    'price_margin_bottom': 3,
    'price_show': True,
    'barcode_width': 140,
    'barcode_show': 140,
    'padding_left': 8,
    'padding_right': 8,
    'padding_top': 8,
    'padding_bottom': 8
}


request_includes = {
    'padding_left': ['6'],
    'padding_bottom': ['8'],
    'padding_top': ['8'],
    'padding_right': ['6'],
    'code_show': ['on'],
    'name_show': ['on'],
    'price_show': ['on'],
    'barcode_show': ['on'],
    'code_font_size': ['10', '10'],
    'code_font_color': ['#FF49C2', '#000000'],
    'code_font_weight': ['bold', 'normal'],
    'name_font_size': ['14'],
    'name_font_color': ['#303030'],
    'name_font_weight': ['bold'],
    'price_font_size': ['15'],
    'price_font_color': ['#000000'],
    'price_font_weight': ['bold']
}

options_dict = {
    'code_font_size': '10',
    'code_font_weight': 'normal',
    'code_font_color': '#FFB4E8',
    'code_show': 'on',
    'name_font_size': '10',
    'name_font_weight': 'normal',
    'name_font_color': '#301120',
    'name_show': 'on',
    'price_font_size': '12',
    'price_font_weight': 'bold',
    'price_font_color': '#FF7A2D',
    'price_show': 'on',
    'barcode_show': 'on',
    'padding_left': '4',
    'padding_right': '11',
    'padding_top': '14',
    'padding_bottom': '12'
}

options_dict = {
    'code_font_size': 10,
    'code_font_weight': 'bold',
    'code_font_color': '#000000',
    'code_show': 'on',
    'name_font_size': 10,
    'name_font_weight': 'bold',
    'name_font_color': '#303030',
    'price_font_size': 17,
    'price_font_weight': 'bold',
    'price_font_color': '#7E1A2E',
    'price_show': 'on',
    'barcode_show': 'on',
    'padding_left': 8,  # 32
    'padding_right': 8,
    'padding_top': 25,
    'padding_bottom': 8
}


options_before = {'frame_padding': 8, 'frame_width': 200, 'frame_height': 125, 'code_font_size': 10, 'code_font_weight': 'bold', 'code_font_color': '#000000', 'code_margin_bottom': 3, 'code_show': True, 'name_font_size': 10, 'name_font_weight': 'bold', 'name_font_color': '#303030',
                  'name_margin_bottom': 3, 'name_show': True, 'price_font_size': 15, 'price_font_weight': 'bold', 'price_font_color': '#000000', 'price_margin_bottom': 3, 'price_show': True, 'barcode_width': 135, 'barcode_show': 140, 'padding_left': 8, 'padding_right': 8, 'padding_top': 6, 'padding_bottom': 8}
options_after = {'frame_padding': 8, 'frame_width': 600, 'frame_height': 375, 'code_font_size': 30, 'code_font_weight': 'bold', 'code_font_color': '#000000', 'code_margin_bottom': 9,
                 'code_show': True, 'name_font_size': 30, 'name_font_weight': 'bold', 'name_font_color': '#303030', 'name_margin_bottom': 9, 'name_show': True, 'price_font_size': 45, 'price_font_weight': 'bold', 'price_font_color': '#000000', 'price_margin_bottom': 9, 'price_show': True, 'barcode_width': 405, 'barcode_show': 140, 'padding_left': 72, 'padding_right': 72, 'padding_top': 54, 'padding_bottom': 72}
