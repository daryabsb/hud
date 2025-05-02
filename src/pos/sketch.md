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