# import stripe

from src.settings.components.env import config

# STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
# stripe.api_key = STRIPE_SECRET_KEY


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
