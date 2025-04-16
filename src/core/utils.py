# import stripe

import random
import ast
from src.settings.components.env import config

# STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
# stripe.api_key = STRIPE_SECRET_KEY


def get_columns(app_name, fields=None, qs=None, actions=False):
    from src.configurations.models import AppTableColumn
    if not qs:
        qs = AppTableColumn.objects.filter(
            is_enabled=True, app__name=app_name
        )
    if fields:
        qs = qs.filter(name__in=fields)

    columns = [
        {
            "id": index,
            "data": column.related_value if column.is_related else column.name,
            "name": column.name,
            "title": column.title,
            "searchable": column.searchable,
            "orderable": column.orderable,
        } for index, column in enumerate(qs)
    ]
    if actions:
        columns.append({
            "id": len(columns) + 1,
            "data": 'actions',
            "name": 'actions',
            "title": 'Actions',
            "searchable": False,
            "orderable": False,
        })
    return columns


def get_indexes(app_name, qs=None, fields=None, actions=None):
    from src.configurations.models import AppTableColumn

    if not qs:
        qs = AppTableColumn.objects.filter(
            is_enabled=True, app__name=app_name
        )
    if fields:
        qs = qs.filter(name__in=fields)

    indexes = {column.name: index for index, column in enumerate(qs)}
    if app_name == 'documents':
        indexes['product'] = len(indexes)
    indexes['start_date'] = len(indexes)
    indexes['end_date'] = len(indexes)
    if actions:
        indexes['actions'] = len(indexes)
    return indexes


def get_fields(app_name, fields=None):
    from src.configurations.models import AppTableColumn
    queryset = AppTableColumn.objects.filter(
        is_enabled=True, app__name=app_name
    )
    if fields:
        queryset = queryset.filter(name__in=fields)
    return [column.related_value if column.is_related else column.name for column in queryset]


def get_searchable_fields(app_name, fields=None, actions=False):
    from src.configurations.models import AppTableColumn
    queryset = AppTableColumn.objects.filter(
        is_enabled=True, app__name=app_name, searchable=True
    )

    indexes = get_indexes(app_name, fields=fields,
                          qs=queryset, actions=actions)
    columns = get_columns(app_name, fields=fields,
                          qs=queryset, actions=actions)
    fields = get_fields(app_name, fields=fields)

    return fields, columns, indexes


def generate_number(target=None, code=''):
    from datetime import date
    min = 100
    max = 3999
    digits = str(random.randint(min, max))
    digits = (len(str(max))-len(digits))*'0'+digits

    if not target:
        target = 'order'
    # print(request.user.id)
    # print(date.today().strftime("%A %d. %B %Y"))
    # print(date.today().strftime("%d%m%Y"))

    if code:
        code = f'{code}-'

    return f'{target}-{code}{date.today().strftime("%d%m%Y")}-{digits}'


def generate_ean13():
    from src.products.models import Barcode
    while True:
        ean = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        checksum = calculate_ean13_checksum(ean)
        ean13 = ean + str(checksum)
        if not Barcode.objects.filter(value=ean13).exists():
            print(ean13)
            return ean13

# For configuration model


def convert_value(value):
    try:
        # Attempt to evaluate the value to its original type
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If evaluation fails, return the value as-is (it is a string)
        return value


def calculate_ean13_checksum(ean):
    # Calculate the checksum for the EAN-13 barcode
    sum_odd = sum(int(ean[i]) for i in range(0, 12, 2))
    sum_even = sum(int(ean[i]) for i in range(1, 12, 2))
    checksum = (10 - (sum_odd + sum_even * 3) % 10) % 10
    return checksum

# def product_sales_pipline(product_name="Test product", product_price=1000):
#     stripe_product_obj = stripe.Product.create(name=product_name)
#     stripe_product_id = stripe_product_obj.id
#     stripe_price_obj = stripe.Price.create(
#         product=stripe_product_id,
#         unit_amount=product_price,
#         currency="usd"
#     )
#     stripe_price_id = stripe_price_obj.id
#     base_endpoint = "http://127.0.0.1:8000"
#     success_url = f"{base_endpoint}/purchases/success/"
#     cancel_url = f"{base_endpoint}/purchases/stopped/"
#     checkou_session = stripe.checkout.Session.create(
#         line_items=[
#             {
#                 "price": stripe_price_id,
#                 "quantity": 1,
#             }
#         ],
#         mode="payment",
#         success_url=success_url,
#         cancel_url=cancel_url
#     )
#     print(checkou_session.url)


def slugify_function(content):
    return content.replace('_', '-').lower()


def add_spaces(input_string):
    spaced_string = ''
    for i, char in enumerate(input_string):
        spaced_string += char
        if (i + 1) % 4 == 0 and i != len(input_string) - 1:
            spaced_string += ' '
    return spaced_string


def remove_spaces(input_string):
    return input_string.replace(' ', '')


def has_spaces(input_string):
    return ' ' in input_string


def hungary_notation(text):
    """
    驼峰表示法 -> 匈牙利表示法

    :param text:
    :return:
    """
    import re
    text_list = list(text)
    for m in sorted((re.finditer('[A-Z]', text)), key=(lambda x: x.span()), reverse=True):
        text_list[m.start():m.end()] = '_' + str(m.group()).lower()

    formatted = ''.join(text_list).strip('_')
    return formatted


def remove_duplicate_elements(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not x in seen if not seen_add(x)]


def get_args_form_dict(key, _dict, expect_type, default=None):
    value = _dict.get(key, default)
    if not isinstance(value, expect_type):
        if not isinstance(default, expect_type):
            value = expect_type()
        else:
            value = default
    return value


def create_store_license_data(store):
    from django.utils import timezone
    now = timezone.now()
    user_plans = store.user_plans.all()

    store_data = {
        'number': str(store.number),
        'user': store.user.id,
    }
    user_plans_list = []
    for userplan in user_plans:
        if not userplan:
            break
        plan_data = {
            'number': str(userplan.number),
            'plan_name': userplan.subscription.name,
            # 'activation_code': userplan.activation_code.code,
            'expiry': '',
            'expired': False
        }
        if userplan.expiry is not None:
            plan_data['expiry'] = userplan.expiry.strftime('%Y-%m-%d %H:%M:%S')
            plan_data['expired'] = userplan.expiry < now

        user_plans_list.append(plan_data)
    store_data["user_plans"] = user_plans_list

    return store_data


def get_num_from_list(a_list):
    container = []
    for item in a_list:
        try:
            container.append(int(item))
        except ValueError:
            pass

    if not container:
        container.append(0)
    return container


'''
sample >>> create_store_license_data =
{
    'user': 2, 
    'store': 'a0b1e522-3230-4e27-af9c-39fe3bac50b5', 
    'user_plans': [
        {
            'number': 'f104fb24-4b0d-484e-a759-541a19c36f45', 
            'plan_name': 'Network Software-Monthly', 
            'activation_code': 'ba58fecb-8a06-48cb-9e1c-447a78e21b9e', 
            'expiry': datetime.datetime(2024, 1, 27, 9, 58, 26, 368057, tzinfo=datetime.timezone.utc)}, 
        {
            'number': 'a65763ee-3ee8-4eef-a8ba-9e8566c4eb16', 
            'plan_name': 'My Logo - Annual Plan', 
            'activation_code': '245e9a1d-e33d-468c-baf8-0e32f4a33a30', 
            'expiry': datetime.datetime(2024, 10, 28, 9, 18, 32, 109328, tzinfo=datetime.timezone.utc)
        }
    ]
}

from src.core.models import User, Store
from src.core.utils import create_store_license_data
user = User.objects.get(id=2)
store = Store.objects.filter(user=user).first()
data = create_store_license_data(store)
data    
'''
