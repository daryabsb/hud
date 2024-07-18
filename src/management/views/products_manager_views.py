from collections import defaultdict
import os
from django.conf import settings
from html2image import Html2Image  # Or imgkit
from django.template.loader import render_to_string
from django.urls import reverse
from src.management.utils import generate_barcode
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from src.products.models import Product, ProductGroup, ProductComment, Barcode
from src.tax.models import ProductTax, Tax
from src.stock.models import StockControl
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


options = {
    'frame_padding': 8,
    'frame_width': 200,
    'frame_height': 125,

    'code_font_size': 10,
    'code_font_weight': 'bold',
    'code_font_color': 'black',
    'code_margin_bottom': 3,
    'code_show': True,

    'name_font_size': 10,
    'name_font_weight': 'bold',
    'name_font_color': 'black',
    'name_margin_bottom': 3,
    'name_show': True,

    'price_font_size': 15,
    'price_font_weight': 'bold',
    'price_font_color': 'black',
    'price_margin_bottom': 3,
    'price_show': True,

    'barcode_width': 140,
}


def render_price_tag(product, options={}):
    return render_to_string('mgt/products/price-tags/partials/price_tag.html', {
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

        print("value type", type(options_dict["value"]))
        print("value is", options_dict["value"])

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
            "html": render_price_tag(product, options)
        }
        tags.append(tag)

    form = PriceTagForm()

    context = {'tags': tags, 'products': products,
               'groups': groups, 'option_forms': option_forms}
    return render(request, 'mgt/products/price-tags/price-tag-control.html', context)


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
    'code_font_color': 'black',
    'code_margin_bottom': 3,
    'code_show': True,

    'name_font_size': 10,
    'name_font_weight': 'bold',
    'name_font_color': 'black',
    'name_margin_bottom': 3,
    'name_show': False,

    'price_font_size': 15,
    'price_font_weight': 'bold',
    'price_font_color': 'black',
    'price_margin_bottom': 3,
    'price_show': True,

    'barcode_width': 140,
    'barcode_show': 140}
