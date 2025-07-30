from .main import (
    pos_home, pos_order, )

from src.pos2.views.order_views import (
    StatusUpdateView,
    CommentUpdateView,
    InternalNoteUpdateView,
)

from .htmx_views import (
    change_quantity,
    add_quantity_on_db,
    subtract_quantity_on_db,
    add_quantity,
    subtract_quantity,
    focus_input,
    remove_item,
    delete_order_item_with_no_response,
    add_order_item,
    AddOrderItemView,
    activate_order,
    order_discount,
    item_discount,
    update_status,
)

from .search_views import (
    search_stock,
    search_customers
)

from .modal_views import (
    pos_search_modal,
)

__all__ = [
    'pos_home', 'pos_order',
    'StatusUpdateView', 'CommentUpdateView', 'InternalNoteUpdateView',
    # HTMX
    'change_quantity', 'add_quantity_on_db', 'subtract_quantity_on_db',
    'add_quantity', 'subtract_quantity', 'focus_input', 'remove_item',
    'delete_order_item_with_no_response', 'add_order_item', 'AddOrderItemView', 'activate_order',
    'order_discount', 'item_discount', 'update_status',
    # SEARCH
    'search_stock', 'search_customers',
    # MODAL
    'pos_search_modal',
]
