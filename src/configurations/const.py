

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
]
