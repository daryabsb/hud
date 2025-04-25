
from django.urls import path, include
from src.pos.views import (
    pos_home,
    # htmx views
    add_item_with_barcode, add_order_item, change_quantity,
    add_quantity, subtract_quantity, remove_item,
    # modal views
    modal_product, modal_order_item, modal_calculator, calculate, add_digit, modal_keyboard,
    add_order_comment, add_order_customer, add_order_payment,
    delete_order_item_with_no_response, activate_order,
    order_discount, calculator_modal, toggle_modal_comment,
    pos_search_modal, pos_order, search_stock,
)


app_name = "pos"

urlpatterns = [
    path('', pos_home, name='pos-home'),
    path('<str:number>/', pos_home, name='pos-order'),
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
    path('order-discount/', order_discount,
         name="order-discount"),
]

# MODALS
urlpatterns += [
    path('modal-order-item/<str:number>/',
         modal_order_item, name="modal-order-item"),
    #     path('modal-calculator/', modal_calculator, name="modal-calculator"),
    path('modals/modal-calculator/', calculator_modal, name="modal-calculator"),
    path('modals/modal-keyboard/', modal_keyboard, name="modal-keyboard"),
    path('modals/calculate/', calculate, name='calculate'),
    path('modals/add_digit/', add_digit, name='add_digit'),

    path('modals/add-order-comment/<str:order_number>/',
         add_order_comment, name='add-order-comment'),
    path('modal-comment/<str:order_number>/',
         toggle_modal_comment, name='modal-comment'),
    path('modals/add-order-customer/<str:order_number>/',
         add_order_customer, name='add-order-customer'),
    path('modals/modal-order-payment/<str:order_number>/',
         add_order_payment, name='modal-order-payment'),
    path('modals/pos-modal-search/', pos_search_modal, name='pos-modal-search'),
    #     actual product modal
    path('modal-product/<int:id>/', modal_product, name="modal-product"),
    path('search/stocks/',
         search_stock, name="modal-search-stocks"),
]


# SEARCH VIEWS
# urlpatterns += [
# ]
