

SECTIONS_INITIAL_DATA = [
    {"id": 1, "name": "application", "icon": 'fab,microsoft'},
    {"id": 2, "name": "messages", "icon": 'fas,envelope'},
    {"id": 3, "name": "business_day", "icon": 'fab,business-time'},
    {"id": 4, "name": "button_bar", "icon": 'fab,business-time'},
]


SETTINGS_INITIAL_DATA = [
    # Application
    {"id": 1, "name": "language", "value": 'en-US', "title": 'Language', "input_type": 'select', "params": 'English,Arabic,Kurdish', "description": '', 'section': 'application'},
    {"id": 2, "name": "writing_direction", "value": 'Left to right', "title": 'Writing Direction', "input_type": 'select', "params": 'Left to write,Right to left', "description": '', 'section': 'application'},
    {"id": 3, "name": "color_scheme", "value": 'dark', "title": 'Color Scheme', "input_type": 'select', "params": 'dark,light,contrast', "description": '', 'section': 'application'},
    {"id": 4, "name": "layout", "value": 'visual', "title": 'Layout', "input_type": 'select', "params": 'visual,standard', "description": '', 'section': 'application'},
    {"id": 5, "name": "num_of_rows", "value": '5', "title": 'Number of rows', "input_type": 'number', "params": '', "description": '', 'section': 'application'},
    {"id": 6, "name": "num_of_cols", "value": '5', "title": 'Number of columns', "input_type": 'number', "params": '', "description": '', 'section': 'application'},
    {"id": 7, "name": "virtual_keyboard", "value": 'False', "title": 'Enable virtual keyboard', "input_type": 'checkbox', "params": '', "description": '', 'section': 'application'},
    {"id": 8, "name": "zoom", "value": '100%', "title": 'Zoom', "input_type": 'select', "params": '150%,125%,100%,75%,500%', "description": '', 'section': 'application'},
    # Messages
    {"id": 9, "name": "show_close_button", "value": 'True', "title": 'Show "Close" button', "input_type": 'checkbox', "params": '', "description": '', 'section': 'messages'},
    {"id": 10, "name": "click_to_close", "value": 'False', "title": 'Click to close', "input_type": 'checkbox', "params": '', "description": '', 'section': 'messages'},
    {"id": 11, "name": "slide_in", "value": 'True', "title": 'Slide in', "input_type": 'checkbox', "params": '', "description": '', 'section': 'messages'},
    {"id": 12, "name": "duration", "value": '5', "title": 'Message duration (sec.)', "input_type": 'number', "params": '', "description": '', 'section': 'messages'},
    {"id": 13, "name": "position", "value": 'Top', "title": 'Position', "input_type": 'select', "params": 'Top,Bottom,Left,Right', "description": '', 'section': 'messages'},
]
