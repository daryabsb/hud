from src.configurations.models import get_menus
from src.orders.models import PosOrder, PosOrderItem
from src.products.models import Product, ProductGroup
from src.documents.models import DocumentType
from src.finances.models import PaymentType
from src.pos.utils import get_active_order
from src.accounts.models import Customer
from django.db.models import Prefetch


def create_new_order(user, document_type=None):
    if not document_type:
        document_type = DocumentType.objects.get(code=200)
    order = PosOrder(user=user, document_type=document_type, is_active=False)
    order.save(doc_type=document_type.name.lower())

    return order


def get_menu_list(user=None):
    
    return get_menus(user)


def get_pos_orders(user=None):
    items_qs = PosOrderItem.objects.select_related('product')
    return PosOrder.objects.filter(
        user=user, is_enabled=True
    ).prefetch_related(
        Prefetch('items', queryset=items_qs, to_attr='order_items')
    ).select_related('user', 'customer').order_by('-date')


def get_product_list(user=None):
    return Product.objects.filter(
        is_enabled=True
    ).select_related('user', 'parent_group', 'currency', 'barcode')


def get_product_groups(user=None):
    return ProductGroup.objects.filter(
        parent__isnull=True
    ).select_related('user').order_by('rank')


def get_customer_list(user=None):
    return Customer.objects.filter.filter(
        is_enabled=True
    ).select_related('user')


def get_payment_types(user=None):
    from src.finances.models.models_payment_type import get_tree_nodes
    return get_tree_nodes()


def get_first_payment_type(user=None):
    return get_payment_types()[0]

# Add your actual implementation for this


def get_active_order(user=None):
    # Placeholder
    return None


# Context bank mapping
CONTEXT_BANK = {
    'active_order': get_active_order,
    'orders': get_pos_orders,
    'products': get_product_list,
    'groups': get_product_groups,
    'customers': get_customer_list,
    'payment_types': get_payment_types,
    'payment_type': get_first_payment_type,
    'menus': get_menu_list,
}


def context_factory(context_keys, user, context=None):
    """
    Generate user-specific context dictionary based on provided keys and merge with existing context.
    """
    if not user:
        raise ValueError("User is required to generate context")

    context = context or {}
    context.update({key: CONTEXT_BANK.get(key, lambda *_: None)(user)
                   for key in context_keys})
    return context


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
