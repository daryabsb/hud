
from django.urls import path
from src.pos.views import (
    pos_home,
    # htmx views
    add_item_with_barcode, add_order_item,
    # modal views
    modal_product, modal_calculator, calculate, add_digit
)

app_name = "pos"

urlpatterns = [
    path('', pos_home, name='pos-home'),
]

# HTMX VIEWS
urlpatterns += [
    path('add-item/', add_order_item, name="add-item"),
    path('add-item-with-barcode/', add_item_with_barcode,
         name="add-item-with-barcode"),
]

# MODALS
urlpatterns += [
    path('modal-product/<int:id>/', modal_product, name="modal-product"),
    path('modal-calculator/', modal_calculator, name="modal-calculator"),
    path('calculate/', calculate, name='calculate'),
    path('add_digit/', add_digit, name='add_digit'),
]
