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


def _get_orders_from_db(user=None, warehouse=None, customer=None):
    orders = PosOrder.objects.all()

    if user and not (user.is_staff or user.is_superuser):
        orders = orders.filter(user=user)

    if warehouse:
        orders = orders.filter(warehouse=warehouse)

    if customer:
        orders = orders.filter(customer=customer)

    # Prefetch related items to avoid N+1 queries
    orders = orders.prefetch_related(
        Prefetch('items', queryset=PosOrderItem.objects.select_related('product'))
    ).select_related('customer', 'document_type', 'warehouse')

    order_list = []

    for order in orders:
        order_data = {
            "number": order.number,
            "customer_id": order.customer.id if order.customer else None,
            "customer": order.customer.name if order.customer else None,
            "document_type": order.document_type.code if order.document_type else None,
            "warehouse": order.warehouse.name if order.warehouse else None,
            "currency": order.currency,
            "item_subtotal": float(order.item_subtotal),
            "total": float(order.total),
            "date": order.date.isoformat(),
            "reference_document_number": order.reference_document_number,
            "internal_note": order.internal_note,
            "note": order.note,
            "due_date": order.due_date.isoformat(),
            "discount": float(order.discount),
            "discount_type": order.discount_type,
            "discounted_amount": float(order.discounted_amount),
            "discount_sign": order.discount_sign,
            "subtotal_after_discount": float(order.subtotal_after_discount),
            "fixed_taxes": float(order.fixed_taxes),
            "total_tax_rate": float(order.total_tax_rate),
            "total_tax": float(order.total_tax),
            "total": float(order.total),
            "paid_status": order.paid_status,
            "status": order.status.name,
            "status_display": order.status.name,
            "status_class": order.status.get_color_class_display(),
            "is_active": order.is_active,
            "is_enabled": order.is_enabled,
            "created": order.created.isoformat(),
            "updated": order.updated.isoformat(),
            "items": []
        }

        for item in order.items.all():
            order_data["items"].append({
                "number": item.number,
                "product_id": item.product.id if item.product else None,
                "product_name": item.product.name if item.product else None,
                "product_image": item.product.image.url if item.product.image else None,
                "quantity": item.quantity,
                "price": float(item.price),
                "currency": item.product.currency.name if item.product else None,
                "round_number": float(item.round_number),
                "is_locked": item.is_locked,
                "is_enabled": item.is_enabled,
                "is_active": item.is_active,
                "discount": item.discount,
                "discount_type": item.discount_type,
                "discounted_amount": float(item.discounted_amount),
                "discount_sign": item.discount_sign,
                "item_total_before_discount": float(item.item_total_before_discount),
                "item_total": float(item.item_total),
                "is_featured": item.is_featured,
                "voided_by": item.voided_by,
                "comment": item.comment,
                "bundle": item.bundle,
                "created": item.created.isoformat(),
                "updated": item.updated.isoformat(),
            })

        order_list.append(order_data)

    return order_list

