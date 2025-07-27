from .main import (
    pos_home, pos_order, )

from src.pos2.views.order_views import (
    StatusUpdateView,
    CommentUpdateView,
    InternalNoteUpdateView,
)

__all__ = [
    'pos_home', 'pos_order',
    'StatusUpdateView', 'CommentUpdateView', 'InternalNoteUpdateView'
]
