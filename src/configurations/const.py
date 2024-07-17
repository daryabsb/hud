

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
    {"id": 50, "name": "code_font_color", "value": 'black', "title": 'Product code font color',
        "input_type": 'text', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 51, "name": "code_margin_bottom", "value": '3', "title": 'Product code bottom margin',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 52, "name": "code_show", "value": 'True', "title": 'Show product code',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 53, "name": "name_font_size", "value": '10', "title": 'Product name font size',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 54, "name": "name_font_weight", "value": 'bold', "title": 'Product name font weight',
        "input_type": 'select', "params": 'bold,normal', "description": '', 'section': 'price_tags'},
    {"id": 55, "name": "name_font_color", "value": 'black', "title": 'Product name font color',
        "input_type": 'text', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 56, "name": "name_margin_bottom", "value": '3', "title": 'Product name bottom margin',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 57, "name": "name_show", "value": 'False', "title": 'Show product name',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 58, "name": "price_font_size", "value": '15', "title": 'Product price font size',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 59, "name": "price_font_weight", "value": 'bold', "title": 'Product price font weight',
        "input_type": 'select', "params": 'bold,normal', "description": '', 'section': 'price_tags'},
    {"id": 60, "name": "price_font_color", "value": 'black', "title": 'Product price font color',
        "input_type": 'text', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 61, "name": "price_margin_bottom", "value": '3', "title": 'Product price bottom margin',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 62, "name": "price_show", "value": 'True', "title": 'show product price',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 63, "name": "barcode_width", "value": '140', "title": 'Barcode width',
        "input_type": 'number', "params": '', "description": '', 'section': 'price_tags'},
    {"id": 64, "name": "barcode_show", "value": '140', "title": 'Show barcode',
        "input_type": 'checkbox', "params": '', "description": '', 'section': 'price_tags'},
]

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
