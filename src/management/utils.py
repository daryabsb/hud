from django.contrib.auth.models import Group, Permission
from src.accounts.models import User
from django.contrib.contenttypes.models import ContentType
from src.management.const import list_permissions_template, add_actions_to_models
from copy import deepcopy


def populate_users_permissions(users=None):
    list_permissions = add_actions_to_models(list_permissions_template)
    if not users:
        users = User.objects.all()

    users_permissions = [{'user': user, 'list_permissions': deepcopy(
        list_permissions)} for user in users]

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


def populate_groups_permissions(groups=None):
    list_permissions = add_actions_to_models(list_permissions_template)

    if not groups:
        groups = Group.objects.all()

    groups_count = groups.count

    groups_permissions = [{'group': group, 'list_permissions': deepcopy(
        list_permissions)} for group in groups]

    for group_perm in groups_permissions:
        list_permissions = group_perm['list_permissions']

        for app_data in list_permissions:
            app_label = app_data['app_label']
            models_data = app_data['models']

            for model_data in models_data:
                model_name = model_data['model']

                # Retrieve ContentType for the model
                try:
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model_name)

                    # Retrieve permissions associated with this ContentType for the group
                    permissions = Permission.objects.filter(
                        content_type=content_type, group=group_perm['group'])

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
    # groups_permissions['count'] = groups_count

    return groups_permissions
