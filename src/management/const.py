import datetime
import random

APP_LIST = []
# Define the list_permissions template
BASE_ACTIONS = [
    {'name': 'add', 'state': False},
    {'name': 'change', 'state': False},
    {'name': 'view', 'state': False},
    {'name': 'delete', 'state': False},
]


def add_actions_to_models(list_permissions_template):
    for app in list_permissions_template:
        for model in app['models']:
            model['actions'] = [action.copy() for action in BASE_ACTIONS]
    return list_permissions_template


list_permissions_template = [
    {
        'app_label': 'accounts',
        'models': [
            {'model': 'user'},
            {'model': 'company'},
        ]
    },
    {
        'app_label': 'tax',
        'models': [
            {'model': 'tax'},
            {'model': 'producttax'},
        ]
    },
]


def generate_filename(model_name,queryset_length):
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    random_number = random.randint(1000, 9999)
    filename = f'{model_name}-{date_str}-{queryset_length}-{random_number}'
    return filename

#  DESIRED TABLES ORDERS
PRODUCTS_DESIRED_ORDER = [
    'id', 
    'code', 
    'name', 
    'slug', 
    'barcode', 
    'parent_group', 
    'price', 
    'cost', 
    'last_purchase_price', 
    'margin', 
    'measurement_unit', 
    'currency', 
    'rank', 
    'plu', 
    'user', 
    'color', 
    'description', 
    'is_tax_inclusive_price', 
    'is_price_change_allowed', 
    'is_service', 
    'is_using_default_quantity', 
    'is_product', 
    'image', 
    'color2', 
    'is_enabled', 
    'age_restriction', 
    'created', 
    'updated'
    ]