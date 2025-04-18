
# const.py
import inspect


def get_view_name():
    return inspect.stack()[2].function  # corrected level for decorator


def get_template_for_view():
    return MY_TEMPLATES.get(get_view_name())


MY_TEMPLATES = {
    'add_new_order': 'cotton/orders/order.html',
    'delete_active_order': 'cotton/orders/order.html',
}
