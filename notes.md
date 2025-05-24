TODO LATER:
- Name shows None when not set - user must input a name at initial setup

# when order is processed (status decides what to do):
- order_status = is_enabled, paid_status, status
- when paid in full: order_status = False, True, Fullfilled (7) => 1 document + 1 payment
- when not paid and customer received the items:
    order_status = True, False, To be paid later (4) => 1 document + 0 payment
- when partially paid (multiple payments created):
    order_status =  True, False, Partially paid (5)
                    => 1 document + multiple payment (for each payment or payment_type)

- orders will be filtered by status:
    - if fullfilled or cancelled: the orders will be filtered (status.ordinal < 7)


## In case of save sale, or payment or quick cash pay
    - a document will be created from the order
    - 


Here’s a comprehensive list of possible **utilities**, **functions**, and **views** you might need to implement full **CRUD functionality** and core **POS operations** for your `PosOrder` and `PosOrderItem` models in your POS app:

---

### 🔁 **CRUD: Core Views (Django Views or DRF API Views)**

#### For `PosOrder`:

* `create_pos_order_view`
* `retrieve_pos_order_view`
* `update_pos_order_view`
* `delete_pos_order_view`
* `list_pos_orders_view`

#### For `PosOrderItem`:

* `create_pos_order_item_view`
* `retrieve_pos_order_item_view`
* `update_pos_order_item_view`
* `delete_pos_order_item_view`
* `list_pos_order_items_view`

---

### 🧠 **Business Logic / Utilities**

* `generate_order_number()` – unique order number generator
* `calculate_order_totals(order)` – central function to update tax, discount, and total
* `apply_order_discount(order, discount, discount_type)`
* `lock_order_items(order)` – mark items as locked once submitted
* `void_order_item(item_id, voided_by_user_id)`
* `bundle_item_parser(bundle_str)` – decode `bundle` field
* `update_order_status(order, new_status)`
* `sync_order_items_with_order_totals(order)` – recalculate subtotal, taxes, etc.

---

### ⚙️ **Helper Views / AJAX Utilities (for HTMX or frontend)**

* `add_product_to_order_view` – adds `PosOrderItem` via AJAX
* `remove_product_from_order_view`
* `change_item_quantity_view`
* `apply_item_discount_view`
* `calculate_item_total_view`
* `get_order_totals_view` – returns updated subtotal, tax, total, etc.
* `list_available_products_view` – modal/product picker for UI
* `search_products_for_order_view`
* `create_customer_from_pos_view` – inline customer creation in POS
* `change_customer_for_order_view`
* `change_order_status_view`

---

### 📊 **Data Views / Reporting**

* `daily_orders_report_view`
* `orders_by_cashier_view`
* `orders_by_customer_view`
* `order_items_summary_view`
* `best_selling_products_view`
* `order_profit_margin_view`

---

### 🔐 **Access & Permissions**

* `is_order_editable(order, user)`
* `can_void_order_item(user)`
* `user_can_discount(order, user)`

---

### 🖨️ **Receipt & Export**

* `generate_order_receipt_pdf_view`
* `print_order_receipt_view`
* `export_order_csv_view`

---

### 🔄 **Status & Workflow**

* `fulfill_order_view`
* `mark_order_as_paid_view`
* `refund_order_view`
* `cancel_order_view`

---

### 🧪 **Testing / Seeds**

* `create_fake_orders(count)`
* `create_test_order_for_user(user)`

---

Let me know if you want these as Django function-based views, class-based views, or DRF views next. You can also specify if this is a single-page POS frontend (like with HTMX or React) to tailor the functions accordingly.
