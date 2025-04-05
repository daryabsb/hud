
from django.urls import path
from src.pos.views import (
    pos_home,
    # htmx views
    add_item_with_barcode, add_order_item, change_quantity,
    add_quantity, subtract_quantity, remove_item,
    # modal views
    modal_product, modal_calculator, calculate, add_digit, modal_keyboard,
    add_order_comment, add_order_customer, add_order_payment,
    delete_order_item_with_no_response, activate_order,
)

app_name = "pos"

urlpatterns = [
    path('', pos_home, name='pos-home'),
]

# HTMX VIEWS
urlpatterns += [
    path('change-quantity/<item_number>/',
         change_quantity, name="change-quantity"),
    path('add-quantity/<item_number>/', add_quantity, name="add-quantity"),
    path('subtract-quantity/<item_number>/',
         subtract_quantity, name="subtract-quantity"),
    path('remove-item/<str:item_number>/',
         remove_item, name="remove-item"),
    path('add-item/', add_order_item, name="add-item"),
    path('add-item-with-barcode/', add_item_with_barcode,
         name="add-item-with-barcode"),
    path('delete-order-item/<str:item_number>/', delete_order_item_with_no_response,
         name="delete-order-item"),
    path('activate-order/<str:order_number>/', activate_order,
         name="activate-order"),
]

# MODALS
urlpatterns += [
    path('modal-product/<str:number>/', modal_product, name="modal-product"),
    path('modal-calculator/', modal_calculator, name="modal-calculator"),
    path('modal-keyboard/', modal_keyboard, name="modal-keyboard"),
    path('calculate/', calculate, name='calculate'),
    path('add_digit/', add_digit, name='add_digit'),

    path('add-order-comment/<str:order_number>/',
         add_order_comment, name='add-order-comment'),
    path('add-order-customer/<str:order_number>/',
         add_order_customer, name='add-order-customer'),
    path('modal-order-payment/<str:order_number>/',
         add_order_payment, name='modal-order-payment'),
]
