
# const.py
import inspect

ORDER_STATUS = (
    (1, 'Unfulfilled'),
    (2, 'Ready for pickup'),
    (3, 'Ready for delivery'),
    (4, 'Cancelled'),
    (5, 'Fulfilled'),
)


def get_view_name():
    return inspect.stack()[2].function  # corrected level for decorator


def get_template_for_view():
    return MY_TEMPLATES.get(get_view_name())


MY_TEMPLATES = {
    'add_new_order': 'cotton/orders/order.html',
    'delete_active_order': 'cotton/orders/order.html',
}
