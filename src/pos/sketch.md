# active_order:
    - create_active_order
    - clear_active_order
    - add_items_to active_order
    - activate_order
    - lock_active_order
    - save_active_order
    - change_active_order_customer
    - change_active_order_comment
    - void_active_order
    - transfer_items_to_another_order
    - add_discount_to_active_order

# active_item:
    - add_quantity
    - subtract_quantity
    - add_discount
    - remove_item

# orders
    - pos_home: ** context: set of orders is_enabled, status < 4 and more...
    - remove_orders_from_list
    - search_by_customer
    - search_by_date_range
    - search_by_number
    - clear_all_and_start_new_order

#  stocks:
    - retrieve_stock


# views and urls:
    - **pos**:

        '/pos/',                                                pos_home,                               name='pos-home'
        '/pos/<str:number>/',                                   pos_home,                               name='pos-order'
        '/pos/change-quantity/<str:item_number>/',              change_quantity,                        name="change-quantity"
        '/pos/add/item-quantity/<str:item_number>/',            add_quantity,                           name="add-quantity"
        '/pos/subtract/item-quantity/<str:item_number>/',       subtract_quantity,                      name="subtract-quantity"
        '/pos/remove-item/<str:item_number>/',                  remove_item,                            name="remove-item"
        '/pos/add/order-item/',                                 add_order_item,                         name="add-item"
        '/pos/delete-order-item/<str:item_number>/',            delete_order_item_with_no_response,     name="delete-order-item"
        '/pos/activate-order/<str:order_number>/',              activate_order,                         name="activate-order"
        '/pos/order-discount/',                                 order_discount,                         name="order-discount"

        '/pos/modal-order-item/<str:number>/',                  modal_order_item,                       name="modal-order-item"
        '/pos/modals/modal-calculator/',                        calculator_modal,                       name="modal-calculator"
        '/pos/modals/modal-keyboard/',                          modal_keyboard,                         name="modal-keyboard"
        '/pos/modals/calculate/',                               calculate,                              name='calculate'
        '/pos/modals/add_digit/',                               add_digit,                              name='add_digit'

        '/pos/modals/add-order-comment/<str:order_number>/',    add_order_comment,                      name='add-order-comment'
        '/pos/modal-comment/<str:order_number>/',               toggle_modal_comment,                   name='modal-comment'
        '/pos/modals/add-order-customer/<str:order_number>/',   add_order_customer,                     name='add-order-customer'
        '/pos/modals/modal-order-payment/<str:order_number>/',  add_order_payment,                      name='modal-order-payment'
        '/pos/modals/pos-modal-search/',                        pos_search_modal,                       name='pos-modal-search'

        '/pos/modal-product/<int:id>/',                         modal_product,                          name="modal-product"
        '/pos/search/stocks/',                                  search_stock,                           name="modal-search-stocks"
