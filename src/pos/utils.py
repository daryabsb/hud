import platform
import uuid
from django.db import transaction
from src.accounts.models import Customer
import after_response

def activate_order(user, order_number):
    from src.orders.models import PosOrder
    PosOrder.objects.filter(
            pk=order_number, user=user).update(is_active=True)
        # Deactivate others
    PosOrder.objects.filter(user=user).exclude(
            pk=order_number).update(is_active=False)
    active_order = PosOrder.objects.get(pk=order_number)
    active_order.refresh_cache()

def get_computer_info():
    computer_name = platform.node()
    machine_id = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return computer_name, machine_id


def get_active_item(item_number=None,  active_order=None):
    from src.orders.models import PosOrderItem
    
    return [item for item in active_order['items'] if item['number'] == item_number][0]

def get_active_order(user, active_order=None):
    from src.orders.models import get_orders
    orders = [order for order in get_orders(user)]
    active_order = next(
        (item for item in orders if item["is_active"] == True), None)
    if active_order is None:
        print("No active order found")
        return {}
    return active_order


def activate_order_and_deactivate_others(user, order_number=None):
    from src.orders.models import PosOrder, get_orders

    if order_number:
        activate_order(user, order_number)
    elif not active_order:
        customer = Customer.objects.first()
        active_order = PosOrder.objects.create(
            user=user, customer=customer, is_active=True)  
    active_order = get_active_order(user=user)
    return active_order


def get_context(active_order):
    from src.pos.calculations import update_order_totals
    order, discount, tax_amount, tax_rate = update_order_totals(active_order)
    return {
        "active_order": order,
        "discount": discount,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "dscnt": tax_amount
    }


# QWERTY keyboard layout with shift, space, caps lock, and enter
qwerty = [
    # Top row: numbers, tick, and brackets
    [
        {"small": "`", "capital": "~", "width": 6, "keycode": 49},
        {"small": "1", "capital": "!", "width": 7, "keycode": 49},
        {"small": "2", "capital": "@", "width": 7, "keycode": 50},
        {"small": "3", "capital": "#", "width": 7, "keycode": 51},
        {"small": "4", "capital": "$", "width": 7, "keycode": 52},
        {"small": "5", "capital": "%", "width": 7, "keycode": 53},
        {"small": "6", "capital": "^", "width": 7, "keycode": 54},
        {"small": "7", "capital": "&", "width": 7, "keycode": 55},
        {"small": "8", "capital": "*", "width": 7, "keycode": 56},
        {"small": "9", "capital": "(", "width": 7, "keycode": 57},
        {"small": "0", "capital": ")", "width": 7, "keycode": 48},
        {"small": "`", "capital": "~", "width": 7, "keycode": 192},
        {"small": "<-", "capital": "<-", "width": 10, "keycode": 221},
    ],
    # QWERTY letters row 1
    [
        {"small": "Tab", "capital": "shift",
            "width": 12, "keycode": 16},  # Left Shift key
        {"small": "q", "capital": "Q", "width": 7, "keycode": 81},
        {"small": "w", "capital": "W", "width": 7, "keycode": 87},
        {"small": "e", "capital": "E", "width": 7, "keycode": 69},
        {"small": "r", "capital": "R", "width": 7, "keycode": 82},
        {"small": "t", "capital": "T", "width": 7, "keycode": 84},
        {"small": "y", "capital": "Y", "width": 7, "keycode": 89},
        {"small": "u", "capital": "U", "width": 7, "keycode": 85},
        {"small": "i", "capital": "I", "width": 7, "keycode": 73},
        {"small": "o", "capital": "O", "width": 7, "keycode": 79},
        {"small": "p", "capital": "P", "width": 7, "keycode": 80},
        {"small": "[", "capital": "{", "width": 7, "keycode": 219},
        {"small": "]", "capital": "}", "width": 7, "keycode": 221},
    ],
    # QWERTY letters row 2
    [
        {"small": "a", "capital": "A", "width": 7, "keycode": 65},
        {"small": "s", "capital": "S", "width": 7, "keycode": 83},
        {"small": "d", "capital": "D", "width": 7, "keycode": 68},
        {"small": "f", "capital": "F", "width": 7, "keycode": 70},
        {"small": "g", "capital": "G", "width": 7, "keycode": 71},
        {"small": "h", "capital": "H", "width": 7, "keycode": 72},
        {"small": "j", "capital": "J", "width": 7, "keycode": 74},
        {"small": "k", "capital": "K", "width": 7, "keycode": 75},
        {"small": "l", "capital": "L", "width": 7, "keycode": 76},
        {"small": "enter", "capital": "enter",
            "width": 16, "keycode": 13},  # Enter key
    ],
    # QWERTY letters row 3
    [
        {"small": "shift", "capital": "shift",
            "width": 13, "keycode": 16},  # Left Shift key
        {"small": "z", "capital": "Z", "width": 7, "keycode": 90},
        {"small": "x", "capital": "X", "width": 7, "keycode": 88},
        {"small": "c", "capital": "C", "width": 7, "keycode": 67},
        {"small": "v", "capital": "V", "width": 7, "keycode": 86},
        {"small": "b", "capital": "B", "width": 7, "keycode": 66},
        {"small": "n", "capital": "N", "width": 7, "keycode": 78},
        {"small": "m", "capital": "M", "width": 7, "keycode": 77},
        {"small": ",", "capital": "<", "width": 7, "keycode": 188},
        {"small": ".", "capital": ">", "width": 7, "keycode": 190},
        {"small": "/", "capital": "?", "width": 7, "keycode": 191},
        {"small": "shift", "capital": "shift",
            "width": 13, "keycode": 16},  # Right Shift key
    ],
    # Space row
    [
        {"small": "caps lock", "capital": "caps lock",
            "width": 13, "keycode": 20},  # Caps Lock key
        {"small": "space", "capital": "space",
            "width": 54, "keycode": 32},  # Space bar
    ],
]
