

SECURITY_KEY_INITIAL_DATA = [
    {"name": "user", "level": 5}
]

direct_save_fields = {"number", "text", "textarea"}
indirect_save_fields = {"checkbox", "radio", "select"}


SECTIONS_INITIAL_DATA = [
    {"id": 1, "name": "application", "icon": 'fab,microsoft',
        "description": 'Settings related to the software.'},
    {"id": 2, "name": "messages", "icon": 'fas,envelope',
        "description": 'Settings related to the messages sent from the server.'},
    {"id": 3, "name": "business_day", "icon": 'fas,business-time',
        "description": 'When a new day starts, a few things needs to be considered.'},
    {"id": 4, "name": "basic_operations", "icon": 'fas,anchor',
        "description": 'This area defines all operations for your app.'},
    {"id": 5, "name": "items", "icon": 'fab,first-order',
        "description": 'This area sets some settings for items.'},
    {"id": 6, "name": "users", "icon": 'fas,user',
        "description": 'This area sets basic settings for users.'},
    {"id": 7, "name": "payment", "icon": 'fas,money-bill',
        "description": 'This area sets basic settings for settings.'},
    {"id": 8, "name": "order_name", "icon": 'fab,first-order',
        "description": 'All settings for order name.'},
    {"id": 9, "name": "products_settings", "icon": 'fab,apple',
        "description": 'This area sets basic settings for settings.'},
    {"id": 10, "name": "weighing_scale", "icon": 'fas,balance-scale',
        "description": 'Wethere you use weighing scal or not, you need some params.'},
    {"id": 11, "name": "customer_display", "icon": 'fas,user-astronaut',
        "description": 'If you have a second display to the user, you need to set it here.'},
    {"id": 12, "name": "price_tags", "icon": 'fas,tags',
        "description": 'This is the default settings for the price tags for the user.'},
]


SETTINGS_INITIAL_DATA = [
    # Application
    {"id": 1, "name": "language", "value": 'en-US', "title": 'Language', "input_type": 'select',
        "params": 'English,Arabic,Kurdish', "description": '', 'section': 'application'},
    {"id": 2, "name": "writing_direction", "value": 'Left to right', "title": 'Writing Direction',
        "input_type": 'select', "params": 'Left to write,Right to left', "description": '', 'section': 'application'},
    {"id": 3, "name": "color_scheme", "value": 'dark', "title": 'Color Scheme', "input_type": 'select',
        "params": 'dark,light,contrast', "description": '', 'section': 'application'},
    {"id": 4, "name": "layout", "value": 'visual', "title": 'Layout', "input_type": 'select',
        "params": 'visual,standard', "description": '', 'section': 'application'},
    {"id": 5, "name": "num_of_rows", "value": '5', "title": 'Number of rows',
        "input_type": 'number', "params": '', "description": '', 'section': 'application'},
    {"id": 6, "name": "num_of_cols", "value": '5', "title": 'Number of columns',
        "input_type": 'number', "params": '', "description": '', 'section': 'application'},
    {"id": 7, "name": "virtual_keyboard", "value": 'False', "title": 'Enable virtual keyboard',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'application'},
    {"id": 8, "name": "zoom", "value": '100%', "title": 'Zoom', "input_type": 'select',
        "params": '150%,125%,100%,75%,500%', "description": '', 'section': 'application'},
    {"id": 9, "name": "button_bar", "value": 'Search,Transfer,Discount,New Sale,Refund,Cash drawer',
        "title": 'Button bar', "input_type": 'checkbox',
        "params": 'Search,Discount,Comment,Refund,Transfer,New Sale,Order name,Cash drawer',
        "description": '* Applicable for "Visual" layout only.', 'section': 'application'},
    # Messages
    {"id": 10, "name": "show_close_button", "value": 'True', "title": 'Show "Close" button',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'messages'},
    {"id": 11, "name": "click_to_close", "value": 'False', "title": 'Click to close',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'messages'},
    {"id": 12, "name": "slide_in", "value": 'True', "title": 'Slide in',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'messages'},
    {"id": 13, "name": "duration", "value": '5',
        "title": 'Message duration (sec.)', "input_type": 'number', "params": '', "description": '', 'section': 'messages'},
    {"id": 14, "name": "position", "value": 'Top', "title": 'Position', "input_type": 'select',
        "params": 'Top,Bottom,Left,Right', "description": '', 'section': 'messages'},
    # Business Day
    {"id": 15, "name": "show_cash", "value": 'False', "title": 'Show cash in on application start',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'business_day'},
    {"id": 16, "name": "show_business_day", "value": 'False', "title": 'Show business day on application start',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'business_day'},
    # Basic Operations
    {"id": 17, "name": "use_floor_plan", "value": 'False', "title": 'Use floor plans',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'basic_operations'},
    {"id": 18, "name": "sounds", "value": 'False', "title": 'Sounds',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'basic_operations'},
    # Itsms
    {"id": 19, "name": "default_search", "value": 'Barcode', "title": 'Default Search',
        "input_type": 'select', "params": 'Name,Barcode,Number', "description": '', 'section': 'items'},
    {"id": 20, "name": "show_search_options", "value": 'True', "title": 'Show search options',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'items'},
    {"id": 21, "name": "default_discount_type", "value": 'Percentage (%)', "title": 'Default discount type',
        "input_type": 'select', "params": 'Percentage (%),Amount ($)', "description": '', 'section': 'items'},
    {"id": 22, "name": "separate_row_for_items", "value": 'False', "title": 'Separate row for each item',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'items'},
    {"id": 23, "name": "prevent_negative_inventory", "value": 'False', "title": 'Prevent negative inventory',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'items'},
    # Users
    {"id": 24, "name": "single_user", "value": 'True', "title": 'Single User',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'users'},
    # Payment
    {"id": 25, "name": "display_receipt_print_dialogue", "value": 'True', "title": 'Display receipt dialog',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'payment'},
    {"id": 26, "name": "default_due_date", "value": '14', "title": 'Default due date',
        "input_type": 'number', "params": '', "description": '', 'section': 'payment'},
    {"id": 27, "name": "merge_items_on_receipt", "value": 'True', "title": 'Merge items on receipt',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'payment'},
    {"id": 28, "name": "single_item_discount", "value": 'True', "title": 'Single item discount allowed',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'payment'},
    {"id": 29, "name": "shortcut_key_payment_confirm", "value": 'True', "title": 'Shortcut keys payment confirmation',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'payment'},
    # products_settings
    {"id": 30, "name": "display_and_print_items_with_tax_included", "value": 'False', "title": 'Display and print items with tax included',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'products_settings'},
    {"id": 31, "name": "discount_apply_rule", "value": 'Before tax', "title": 'Discount apply rule',
        "input_type": 'select', "params": 'Before tax,After tax', "description": '', 'section': 'products_settings'},
    {"id": 32, "name": "sorting", "value": 'Name', "title": 'Sorting',
        "input_type": 'select', "params": 'Name,Code', "description": '', 'section': 'products_settings'},
    {"id": 33, "name": "allow_negative_price", "value": 'True', "title": 'Allow negative price',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'products_settings'},
    {"id": 34, "name": "default_tax_rate", "value": '', "title": 'Default tax rate', "input_type": 'text', "params": '',
        "description": 'Taxes not found. Please add tax rates in management section.', 'section': 'products_settings'},
    {"id": 35, "name": "cost_price_based_markup", "value": 'False', "title": 'Cost price based markup',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'products_settings'},
    {"id": 36, "name": "automatically_update_cost_price_on_purchase", "value": 'False', "title": 'Automatically update cost price on purchase',
        "input_type": 'checkbox', "params": '', "description": "What's this?", 'section': 'products_settings'},
    {"id": 37, "name": "enable_moving_average_price", "value": 'False', "title": 'Enable moving average price',
        "input_type": 'checkbox', "params": '', "description": "What's this?", 'section': 'products_settings'},
    # weighing_scale
    {"id": 38, "name": "enable_weighing_scales_barcode", "value": 'False', "title": 'Enable weighing scales barcode',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'weighing_scale'},
    # customer_display
    {"id": 39, "name": "enabled", "value": 'False', "title": 'Enabled',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'customer_display'},
    {"id": 40, "name": "com_port", "value": 'COM1', "title": 'COM port', "input_type": 'select',
        "params": 'COM1,COM2,COM3', "description": '', 'section': 'customer_display'},
    {"id": 41, "name": "number_of_characters", "value": '20', "title": 'Number of characters',
        "input_type": 'number', "params": '', "description": '', 'section': 'customer_display'},
    {"id": 42, "name": "welcome_message_top_line", "value": 'WELCOME!', "title": 'Top line',
        "input_type": 'text', "params": '', "description": '', 'section': 'customer_display'},
    {"id": 43, "name": "welcome_message_bottom_line", "value": '', "title": 'Bottom line',
        "input_type": 'text', "params": '', "description": '', 'section': 'customer_display'},
    {"id": 44, "name": "test_display", "value": '', "title": 'Test display',
        "input_type": 'button', "params": '', "description": '', 'section': 'customer_display'},
    # pricetags_settings
    {"id": 45, "name": "frame_padding", "value": '8', "title": 'Price tag frame padding',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 46, "name": "frame_width", "value": '200', "title": 'Price tag frame width',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 47, "name": "frame_height", "value": '125', "title": 'Price tag frame height',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 48, "name": "code_font_size", "value": '10', "title": 'Product code font size',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 49, "name": "code_font_weight", "value": 'bold', "title": 'Product code font weight',
        "input_type": 'select', "params": 'bold,normal', "description": '', 'section': 'price_tags'},
    {"id": 50, "name": "code_font_color", "value": '#000000', "title": 'Product code font color',
        "input_type": 'text', "params": 'color', "description": '', 'section': 'price_tags'},
    {"id": 51, "name": "code_margin_bottom", "value": '3', "title": 'Product code bottom margin',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 52, "name": "code_show", "value": 'True', "title": 'Show product code',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 53, "name": "name_font_size", "value": '10', "title": 'Product name font size',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 54, "name": "name_font_weight", "value": 'bold', "title": 'Product name font weight',
        "input_type": 'select', "params": 'bold,normal', "description": '', 'section': 'price_tags'},
    {"id": 55, "name": "name_font_color", "value": '#000000', "title": 'Product name font color',
        "input_type": 'text', "params": 'color', "description": '', 'section': 'price_tags'},
    {"id": 56, "name": "name_margin_bottom", "value": '3', "title": 'Product name bottom margin',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 57, "name": "name_show", "value": 'False', "title": 'Show product name',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 58, "name": "price_font_size", "value": '15', "title": 'Product price font size',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 59, "name": "price_font_weight", "value": 'bold', "title": 'Product price font weight',
        "input_type": 'select', "params": 'bold,normal', "description": '', 'section': 'price_tags'},
    {"id": 60, "name": "price_font_color", "value": '#000000', "title": 'Product price font color',
        "input_type": 'text', "params": 'color', "description": '', 'section': 'price_tags'},
    {"id": 61, "name": "price_margin_bottom", "value": '3', "title": 'Product price bottom margin',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 62, "name": "price_show", "value": 'True', "title": 'show product price',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 63, "name": "barcode_width", "value": '140', "title": 'Barcode width',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 64, "name": "barcode_height", "value": '42', "title": 'Barcode height',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 65, "name": "barcode_show", "value": '140', "title": 'Show barcode',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 66, "name": "padding_left", "value": '8', "title": 'Padding left',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 67, "name": "padding_right", "value": '8', "title": 'Padding right',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 68, "name": "padding_top", "value": '8', "title": 'Padding top',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 69, "name": "padding_bottom", "value": '8', "title": 'Padding bottom',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
]

APP_TABLES = ['products', 'documents', 'document_items']
APP_TABLES_COLUMNS = [
    {"id": 1, "app": "products", "name": "id", "title": "Id",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },
    {"id": 2, "app": "products", "name": "code", "title": "Code",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },
    {"id": 3, "app": "products", "name": "image", "title": "Image",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 4, "app": "products", "name": "name", "title": "Name",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },
    {"id": 5, "app": "products", "name": "slug", "title": "Slug",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 6, "app": "products", "name": "barcode", "title": "Barcode",
        "is_enabled": True, "is_related": True, "related_value": "barcode__value", "searchable": True, },
    {"id": 7, "app": "products", "name": "parent_group", "title": "Parent Group",
        "is_enabled": True, "is_related": True, "related_value": "parent_group__name", "searchable": True, },
    {"id": 8, "app": "products", "name": "price", "title": "Price",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 9, "app": "products", "name": "cost", "title": "Cost",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 10, "app": "products", "name": "last_purchase_price", "title": "Last Purchase Price",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 11, "app": "products", "name": "margin", "title": "Margin",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 12, "app": "products", "name": "measurement_unit", "title": "Measurement Unit",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 13, "app": "products", "name": "currency", "title": "Currency",
        "is_enabled": True, "is_related": True, "related_value": "currency__name", "searchable": False, },
    {"id": 14, "app": "products", "name": "rank", "title": "Rank",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 15, "app": "products", "name": "plu", "title": "Plu",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 16, "app": "products", "name": "user", "title": "User",
        "is_enabled": True, "is_related": True, "related_value": "user__name", "searchable": False, },
    {"id": 17, "app": "products", "name": "color", "title": "Color",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 18, "app": "products", "name": "description", "title": "Description",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 19, "app": "products", "name": "is_tax_inclusive_price", "title": "Is Tax Inclusive Price",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 20, "app": "products", "name": "is_price_change_allowed",
        "title": "Is Price Change Allowed", "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 21, "app": "products", "name": "is_service", "title": "Is Service",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 22, "app": "products", "name": "is_using_default_quantity",
        "title": "Is Using Default Quantity", "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 23, "app": "products", "name": "is_product", "title": "Is Product",
        "is_enabled": False, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 24, "app": "products", "name": "is_enabled", "title": "Is Enabled",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 25, "app": "products", "name": "age_restriction", "title": "Age Restriction",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 26, "app": "products", "name": "created", "title": "Created",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 27, "app": "products", "name": "updated", "title": "Updated",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 28, "app": "documents", "name": "id", "title": "Id",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 29, "app": "documents", "name": "number", "title": "Number",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },

    {"id": 30, "app": "documents", "name": "customer", "title": "Customer",
        "is_enabled": True, "is_related": True, "related_value": "customer__name", "searchable": True, },

    {"id": 31, "app": "documents", "name": "cash_register", "title": "Cash Register",
        "is_enabled": True, "is_related": True, "related_value": "cash_register__name", "searchable": False, },

    {"id": 32, "app": "documents", "name": "order", "title": "Order",
        "is_enabled": True, "is_related": True, "related_value": "order__id", "searchable": True, },

    {"id": 33, "app": "documents", "name": "document_type", "title": "Type",
        "is_enabled": True, "is_related": True, "related_value": "document_type__name", "searchable": True, },

    {"id": 34, "app": "documents", "name": "warehouse", "title": "Warehouse",
        "is_enabled": True, "is_related": True, "related_value": "warehouse__name", "searchable": False, },

    {"id": 35, "app": "documents", "name": "date", "title": "Issued Date",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 36, "app": "documents", "name": "user", "title": "User",
        "is_enabled": True, "is_related": True, "related_value": "user__name", "searchable": False, },

    {"id": 37, "app": "documents", "name": "reference_document_number", "title": "Ref #",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },

    {"id": 38, "app": "documents", "name": "internal_note", "title": "Internal Note",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 39, "app": "documents", "name": "note", "title": "Note",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 40, "app": "documents", "name": "due_date", "title": "Due Date",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 41, "app": "documents", "name": "discount", "title": "Discount",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 42, "app": "documents", "name": "discount_type", "title": "Discount Type",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 43, "app": "documents", "name": "discount_apply_rule", "title": "Discount Rule",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 44, "app": "documents", "name": "paid_status", "title": "Paid Status",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },

    {"id": 45, "app": "documents", "name": "stock_date", "title": "Stock Date",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 46, "app": "documents", "name": "total", "title": "Total",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 47, "app": "documents", "name": "is_clocked_out", "title": "Is Clocked Out",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 48, "app": "documents", "name": "created", "title": "Created",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 49, "app": "documents", "name": "updated", "title": "Updated",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },



    {"id": 50, "app": "document_items", "name": "id", "title": "Id",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },

    {"id": 51, "app": "document_items", "name": "user", "title": "User",
        "is_enabled": True, "is_related": True, "related_value": "user__name", "searchable": True, },

    {"id": 52, "app": "document_items", "name": "document", "title": "Document",
        "is_enabled": False, "is_related": True, "related_value": "document__id", "searchable": True, },

    {"id": 53, "app": "document_items", "name": "product", "title": "Product",
        "is_enabled": True, "is_related": True, "related_value": "product__name", "searchable": True, },

    {"id": 54, "app": "document_items", "name": "quantity", "title": "Quantity",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 55, "app": "document_items", "name": "expected_quantity", "title": "Expected Quantity",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 56, "app": "document_items", "name": "price", "title": "Price",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 57, "app": "document_items", "name": "discount", "title": "Discount",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 58, "app": "document_items", "name": "discount_type", "title": "Discount Type",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 59, "app": "document_items", "name": "product_cost", "title": "Product Cost",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 60, "app": "document_items", "name": "price_before_tax", "title": "Price Before Tax",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 61, "app": "document_items", "name": "price_before_tax_after_discount", "title": "Price BeforeTax After Discount",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 62, "app": "document_items", "name": "price_after_discount", "title": "Price After Discount",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 63, "app": "document_items", "name": "total_after_document_discount", "title": "Total After Document Discount",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 64, "app": "document_items", "name": "total", "title": "Total",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 65, "app": "document_items", "name": "discount_apply_rule", "title": "Discount Apply Rule",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    {"id": 66, "app": "document_items", "name": "returned", "title": "Returned",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },




    {"id": 48, "app": "documents", "name": "created", "title": "Created",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

    {"id": 49, "app": "documents", "name": "updated", "title": "Updated",
        "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

]

[
    'id', 'user', 'document', 'product', 'quantity', 'expected_quantity', 'price_before_tax', 'price',
    'discount', 'discount_type', 'product_cost', 'price_before_tax_after_discount', 'price_after_descount',
    'total', 'total_after_document_discount', 'discount_apply_rule', 'returned', 'created', 'updated'
]
'''
['id', 'number', 'user', 'customer', 'cash_register', 'order', 'document_type', 'warehouse', 
'date', 'reference_document_number', 'internal_note', 'note', 'due_date', 'discount', 
'discount_type', 'discount_apply_rule', 'paid_status', 'stock_date', 'total', 'is_clocked_out', 
'created', 'updated']
'''


'''
payment, fas,money

id  name                            value       title                                    input_type     description     section
25  display_receipt_print_dialogue  True        Display receipt dialog                   checkbox       -               payment
26  default_due_date                14          Default due daye                         number         -               payment
27  merge_items_on_receipt          True        Merge items on receipt                   checkbox       -               payment
28  single_item_discount            True        Single item discount allowed             checkbox       -               payment
29 shortcut_key_payment_confirm     True        Shortcut keys payment confirmation       checkbox       -               payment


('language', 'en-US', 'English,Arabic,Kurdish')
('writing_direction', 'Left to right', 'Left to write,Right to left')
('color_scheme', 'dark', 'dark,light,contrast')
('layout', 'visual', 'visual,standard')
('num_of_rows', '5', '')
('num_of_cols', '5', '')
('virtual_keyboard', 'False', '')
('zoom', '100%', '150%,125%,100%,75%,500%')
('button_bar', 'Search,Transfer,Discount,New Sale,Refund,Cash drawer', 'Search,Discount,Comment,Refund,Transfer,New Sale,Order name,Cash drawer')
('show_close_button', 'True', '')
('click_to_close', 'False', '')
('slide_in', 'True', '')
('duration', '5', '')
('position', 'Top', 'Top,Bottom,Left,Right')
('show_cash', 'False', '')
('show_business_day', 'False', '')
('use_floor_plan', 'False', '')
('sounds', 'False', '')
('default_search', 'Barcode', 'Name,Barcode,Number')
('show_search_options', 'True', '')
('default_discount_type', 'Percentage (%)', 'Percentage (%),Amount ($)')
('separate_row_for_items', 'False', '')
('prevent_negative_inventory', 'False', '')
('single_user', 'True', '')
('display_receipt_print_dialogue', 'True', '')
('default_due_date', '14', '')
('merge_items_on_receipt', 'True', '')
('single_item_discount', 'True', '')
('shortcut_key_payment_confirm', 'True', '')
('display_and_print_items_with_tax_included', 'False', '')
('discount_apply_rule', 'Before tax', 'Before tax,After tax')
('sorting', 'Name', 'Name,Code')
('allow_negative_price', 'True', '')
('default_tax_rate', '', '')
('cost_price_based_markup', 'False', '')
('automatically_update_cost_price_on_purchase', 'False', '')
('enable_moving_average_price', 'False', '')
('enable_weighing_scales_barcode', 'False', '')
('enabled', 'False', '')
('com_port', 'COM1', 'COM1,COM2,COM3')
('number_of_characters', '20', '')
('welcome_message_top_line', 'WELCOME!', '')
('welcome_message_bottom_line', '', '')
('test_display', '', '')

'''
