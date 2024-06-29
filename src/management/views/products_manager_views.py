from collections import defaultdict
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from src.products.models import Product, ProductGroup, ProductComment
from src.tax.models import ProductTax
from django.forms import modelformset_factory
from src.products.forms import (
    ProductGroupForm, ConfirmPasswordForm, ProductDetailsForm,
    BarcodeForm, ProductCommentForm
)
from src.stock.forms import StockControlForm
from src.tax.forms import ProductTaxForm
from src.accounts.forms import CustomerForm
from src.stock.models import Stock
from src.accounts.models import User
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


def mgt_stocks(request):
    stocks = Stock.objects.all()
    return render(request, 'mgt/stocks/list.html', {"stocks": stocks})


list_permissions = [
    {
        'app': 'accounts',
        'models': ['user', 'company']
    },
    {
        'app': 'finances',
        'models': ['tax', 'pos_order']
    },
]


def mgt_users(request):
    from src.management.utils import populate_users_permissions, populate_groups_permissions
    users = User.objects.all()

    permission_list = populate_users_permissions(users)

    groups_list = Group.objects.all()
    lone_group = Group.objects.first()
    groups_permission_list = populate_groups_permissions(groups_list)

    permissions_by_app_model = defaultdict(lambda: defaultdict(list))

    context = {
        "users": users,
        "groups": groups_list,
        "permissions": permission_list,
        "groups_permissions": groups_permission_list,
        'permissions_by_app_model': dict(permissions_by_app_model),
        "list_permissions": list_permissions,
        # "users_with_permissions": users_with_permissions,
        # "groups_with_permissions": groups_with_permissions,
    }
    return render(request, 'mgt/users/list.html', context)


@require_POST
@login_required
def update_product_group(request, slug=None):
    group = None
    if slug:
        group = get_object_or_404(ProductGroup, slug=slug)
    form = ProductGroupForm(request.POST, instance=group)

    if form.is_valid():
        group = form.save(commit=False)
        group.user = request.user
        print("slug is: ", group.slug)
        group.save()
    groups_list = Group.objects.all()
    context = {
        "groups": groups_list,
    }

    return render(request, 'mgt/products/partials/sidebar.html', context)


@require_POST
@login_required
def add_product_group(request):

    group_id = request.POST.get('group-id', None)
    if group_id:
        print("group id from update is: ", group_id)
        group = get_object_or_404(ProductGroup, id=group_id)
        form = ProductGroupForm(request.POST, instance=group)
    else:
        form = ProductGroupForm(request.POST)

    if form.is_valid():
        group = form.save(commit=False)
        group.user = request.user
        group.save()
    groups_list = ProductGroup.objects.all()
    context = {
        "groups": groups_list,
    }

    return render(request, 'mgt/products/partials/sidebar.html', context)


def delete_product_group(request):
    from django.contrib.auth import authenticate
    group_id = request.POST.get('delete-group-id', None)
    form = ConfirmPasswordForm(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user is not None:
            group = get_object_or_404(ProductGroup, id=group_id)
            group.delete()
            groups_list = ProductGroup.objects.all()
            context = {
                "groups": groups_list,
            }
            return render(request, 'mgt/products/partials/sidebar.html', context)

    # group.delete()


def add_product(request):
    if request.method == 'POST':
        product_form = ProductDetailsForm(request.POST, request.FILES)
        barcode_form = BarcodeForm(request.POST)
        product_tax_formset = modelformset_factory(ProductTax, form=ProductTaxForm, extra=1)(request.POST, queryset=ProductTax.objects.none())
        stock_control_form = StockControlForm(request.POST)
        customer_form = CustomerForm(request.POST)
        product_comment_formset = modelformset_factory(ProductComment, form=ProductCommentForm, extra=1)(request.POST, queryset=ProductComment.objects.none())

        if all([
            product_form.is_valid(),
            barcode_form.is_valid(),
            product_tax_formset.is_valid(),
            stock_control_form.is_valid(),
            customer_form.is_valid(),
            product_comment_formset.is_valid()
        ]):
            product = product_form.save()
            barcode = barcode_form.save(commit=False)
            barcode.product = product
            barcode.save()

            for form in product_tax_formset:
                tax = form.save(commit=False)
                tax.product = product
                tax.save()

            stock_control = stock_control_form.save(commit=False)
            stock_control.product = product
            stock_control.save()

            for form in product_comment_formset:
                comment = form.save(commit=False)
                comment.product = product
                comment.save()

            return redirect('product_list')  # Replace 'product_list' with your product list view name

    else:
        product_form = ProductDetailsForm()
        barcode_form = BarcodeForm()
        product_tax_formset = modelformset_factory(ProductTax, form=ProductTaxForm, extra=1)(queryset=ProductTax.objects.none())
        stock_control_form = StockControlForm()
        customer_form = CustomerForm()
        product_comment_formset = modelformset_factory(ProductComment, form=ProductCommentForm, extra=1)(queryset=ProductComment.objects.none())

    return render(request, 'your_template.html', {
        'product_form': product_form,
        'barcode_form': barcode_form,
        'product_tax_formset': product_tax_formset,
        'stock_control_form': stock_control_form,
        'customer_form': customer_form,
        'product_comment_formset': product_comment_formset,
    })












permision_sample = [
    '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
    '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__',
    '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
    '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk',
    '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes',
    '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers',
    '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes',
    '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display',
    '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order',
    '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks',
    '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', '_validate_force_insert',

    'DoesNotExist', 'MultipleObjectsReturned', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields',
    'codename', 'content_type', 'content_type_id', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints',
    'get_deferred_fields', 'group_set',
    'id', 'name', 'natural_key', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base',
    'serializable_value', 'unique_error_message', 'user_set', 'validate_constraints', 'validate_unique'

]
'''
user = {
    'name': 'Super Admin', 
    'email': 'root@root.com', 
    'permissions_form': <PermissionForm bound=False, valid=Unknown, 
        fields=(account_emailaddress_add;account_emailaddress_change;account_emailaddress_delete;
        account_emailaddress_make;account_emailaddress_view;account_emailconfirmation_add;
        account_emailconfirmation_change;account_emailconfirmation_delete;account_emailconfirmation_view;
        accounts_company_add;accounts_company_change;accounts_company_delete;accounts_company_view;
        accounts_country_add;accounts_country_change;accounts_country_delete;accounts_country_view;
        accounts_customer_add;accounts_customer_change;accounts_customer_delete;accounts_customer_view;
        accounts_customerdiscount_add;accounts_customerdiscount_change;accounts_customerdiscount_delete;
        
        # more cut from here to save tokens
       
        tax_tax_delete;tax_tax_view)>, 
    'permissions': defaultdict(<function get_permissions_context.<locals>.<lambda> at 0x00000211C856BC40>, 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         {'account': defaultdict(<class 'list'>, {'emailaddress': ['add', 'change', 'delete', 'make', 'view'], 'emailconfirmation': ['add']})})}
'''
group = [
    'DoesNotExist', 'MultipleObjectsReturned',
    '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__',
    '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__',
    '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', '_validate_force_insert', 'adelete', 'arefresh_from_db', 'asave', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'id', 'name', 'natural_key', 'objects', 'permissions', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'user_set', 'validate_constraints', 'validate_unique']
