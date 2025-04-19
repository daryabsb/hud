from src.orders.models import PosOrder
from src.documents.models import DocumentType
from src.pos.utils import get_active_order


def create_new_order(user, document_type=None):
    if not document_type:
        document_type = DocumentType.objects.get(code=200)
    order = PosOrder(user=user, document_type=document_type, is_active=False)
    order.save(doc_type=document_type.name.lower())

    return order


# Sample context-generating functions

def get_menu_list():
    from src.configurations.models import ApplicationPropertySection
    menus = ApplicationPropertySection.objects.get(name='Menu')
    return menus.application_properties.all()
    

def get_pos_orders():
    from src.orders.models import PosOrder
    return PosOrder.objects.filter(is_enabled=True)


def get_product_list():
    from src.products.models import Product
    return Product.objects.filter(is_enabled=True)


def get_product_groups():
    from src.products.models import ProductGroup
    return ProductGroup.objects.filter(parent__isnull=True)


def get_customer_list():
    return ['John Doe', 'Jane Smith']


def get_payment_types():
    from src.finances.models import PaymentType
    return PaymentType.objects.filter(is_enabled=True)


def get_first_payment_type():
    return get_payment_types().first()


# Define the context bank with functions that generate context data
CONTEXT_BANK = {
    'active_order': get_active_order(),
    'orders': get_pos_orders(),
    'products': get_product_list(),
    'groups': get_product_groups(),
    'customers': get_customer_list(),
    'payment_types': get_payment_types(),
    "payment_type": get_first_payment_type(),
    "menus": get_menu_list(),
}


def context_factory(context_keys, context=None):
    """
    Generate context dictionary based on provided keys and merge with existing context.

    Args:
        context_keys (list): List of context keys needed for the view
        context (dict, optional): Existing context to merge with. Defaults to None.

    Returns:
        dict: Dictionary containing the merged context data
    """
    # Start with the provided context or an empty dict if None
    final_context = context if context is not None else {}

    # Generate context for the requested keys
    for key in context_keys:
        if key in CONTEXT_BANK:
            final_context[key] = CONTEXT_BANK[key]
        else:
            final_context[key] = None

    return final_context


# context = context_factory(needed_context)
# Example usage in a view (assuming Django)
# def context_factory(context_keys, context=None):
#     final_context = context if context is not None else {}

#     for key in context_keys:
#         # Only add the key if it doesn't already exist in the provided context
#         if key not in final_context and key in CONTEXT_BANK:
#             final_context[key] = CONTEXT_BANK[key]()
#         elif key not in CONTEXT_BANK:
#             final_context[key] = None

#     return final_context
