
APP_LIST = []
# Define the list_permissions template
BASE_ACTIONS = [
    {'name': 'add', 'state': False},
    {'name': 'change', 'state': False},
    {'name': 'view', 'state': False},
    {'name': 'delete', 'state': False},
]


def add_actions_to_models(list_permissions_template):
    for app in list_permissions_template:
        for model in app['models']:
            model['actions'] = [action.copy() for action in BASE_ACTIONS]
    return list_permissions_template


list_permissions_template = [
    {
        'app_label': 'accounts',
        'models': [
            {'model': 'user'},
            {'model': 'company'},
        ]
    },
    {
        'app_label': 'finances',
        'models': [
            {'model': 'tax'},
            {'model': 'pos_order'},
        ]
    },
]
