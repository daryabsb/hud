import importlib
from django.conf import settings
from django.apps import apps
from django.contrib.auth.models import Group, Permission
from src.accounts.models import User
from django.contrib.contenttypes.models import ContentType
from src.management.const import list_permissions_template
from copy import deepcopy


def populate_users_permissions(users=None):
    if not users:
        users = User.objects.all()

    users_permissions = [{'user': user, 'list_permissions': deepcopy(
        list_permissions_template)} for user in users]

    for user_perm in users_permissions:
        list_permissions = user_perm['list_permissions']

        for app_data in list_permissions:
            app_label = app_data['app_label']
            models_data = app_data['models']

            for model_data in models_data:
                model_name = model_data['model']

                # Retrieve ContentType for the model
                try:
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model_name)

                    # Retrieve permissions associated with this ContentType for the user
                    permissions = Permission.objects.filter(
                        content_type=content_type, user=user_perm['user'])

                    # Update actions with actual permission values
                    model_actions = model_data['actions']

                    for action in model_actions:
                        # Convert action name to lowercase (e.g., 'add')
                        action_name = action['name'].lower()
                        action['state'] = any(
                            perm.codename == f'{action_name}_{model_name}' for perm in permissions)

                except ContentType.DoesNotExist:
                    # Handle case where ContentType does not exist (should not normally happen)
                    pass

    return users_permissions


def get_app_label(app_name):
    try:
        module = importlib.import_module(f"{app_name}")
        return getattr(module, 'APP_LABEL', app_name.title())
    except ImportError:
        return app_name.title()


def get_list_permissions_template():
    list_permissions_template = []

    for app_config in apps.get_app_configs():
        app_label = app_config.label

        # Only include apps that are in the INSTALLED_APPS
        if app_label in settings.INSTALLED_APPS:
            models = [
                {'model': model._meta.model_name,
                    'verbose_name': model._meta.verbose_name}
                for model in app_config.get_models()
            ]
            app_display_label = get_app_label(app_label)
            list_permissions_template.append({
                'app_label': app_display_label,
                'models': models,
            })

    return list_permissions_template


def run():
    # users_permissions = populate_users_permissions()
    # print(users_permissions)
    list_permissions_template = get_list_permissions_template()
    # print(list_permissions_template)
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if model._meta.verbose_name:
                print(model._meta.verbose_name)
    # for model in apps.all_models:
    #     print(model._meta)
    # print(apps.all_models.keys())


user_pers = [
    {'user': '<User: root@root.com>',
     'list_permissions': [
         {
             'app_label': 'accounts',
             'models': [
                 {
                     'model': 'user', 'add': False, 'change': False, 'view': False, 'delete': False
                 },
                 {
                     'model': 'company', 'add': False, 'change': False, 'view': False, 'delete': False
                 }
             ]
         }, {'app_label': 'finances', 'models': [{'model': 'tax', 'add': False, 'change': True, 'view': True, 'delete': False}, {'model': 'pos_order', 'add': False, 'change': True, 'view': True, 'delete': False}]}]}]
