from collections import defaultdict
from django.shortcuts import render
from src.products.models import Product
from src.products.forms import ProductForm
from src.stock.models import Stock
from src.accounts.models import User
# Create your views here.
from django.contrib.auth.models import Group, Permission


def mgt_products(request):
    products = Product.objects.all()
    return render(request, 'mgt/products/list.html', {"products": products})


def mgt_stocks(request):
    stocks = Stock.objects.all()
    form = ProductForm()
    return render(request, 'mgt/stocks/list.html', {"stocks": stocks, "form": form})


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
