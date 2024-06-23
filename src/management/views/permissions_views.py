from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from src.accounts.models import User
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


@login_required
@require_POST
def mgt_update_permissions(request):
    from src.management.utils import populate_users_permissions
    user_id = request.POST.get('user-id')
    new_permissions = request.POST.getlist('permissions')

    user = get_object_or_404(User, pk=user_id)

    # Extract the current permissions of the user
    current_permissions = user.user_permissions.all()

    # Create sets for easier comparison
    current_permission_codenames = set(
        f"{p.codename}_{p.content_type.app_label}" for p in current_permissions
    )
    new_permission_codenames = set(new_permissions)

    # Permissions to add
    permissions_to_add = new_permission_codenames - current_permission_codenames

    # Permissions to remove
    permissions_to_remove = current_permission_codenames - new_permission_codenames

    # Add new permissions
    for perm in permissions_to_add:
        try:
            action, model, app_label = perm.rsplit('_', 2)
            content_type = ContentType.objects.get(
                app_label=app_label, model=model)
            permission = Permission.objects.get(
                content_type=content_type, codename=f'{action}_{model}')
            user.user_permissions.add(permission)
        except ContentType.DoesNotExist:
            print(f"ContentType not found for {app_label}.{model}")
            continue
        except Permission.DoesNotExist:
            print(f"Permission not found: {perm}")
            continue

    # Remove old permissions
    for perm in permissions_to_remove:
        try:
            print("perm_to_remove: ", perm)
            action, model, app_label = perm.rsplit('_', 2)
            content_type = ContentType.objects.get(
                app_label=app_label, model=model)
            permission = Permission.objects.get(
                content_type=content_type, codename=f'{action}_{model}')
            user.user_permissions.remove(permission)
        except ContentType.DoesNotExist:
            print(f"ContentType not found for {app_label}.{model}")
            continue
        except Permission.DoesNotExist:
            print(f"Permission not found: {perm}")
            continue
    users = User.objects.all()

    permission_list = populate_users_permissions(users)
    context = {
        "permissions": permission_list
    }

    return render(request, 'mgt/users/partials/user-table.html', context)


@login_required
@require_POST
def mgt_update_group_permissions(request):
    from src.management.utils import populate_groups_permissions
    group_id = request.POST.get('group-id')
    new_permissions = request.POST.getlist('permissions')

    group = get_object_or_404(Group, pk=group_id)

    # Extract the current permissions of the user
    current_permissions = group.permissions.all()

    # Create sets for easier comparison
    current_permission_codenames = set(
        f"{p.codename}_{p.content_type.app_label}" for p in current_permissions
    )
    new_permission_codenames = set(new_permissions)

    # Permissions to add
    permissions_to_add = new_permission_codenames - current_permission_codenames

    # Permissions to remove
    permissions_to_remove = current_permission_codenames - new_permission_codenames

    # Add new permissions
    for perm in permissions_to_add:
        try:
            action, model, app_label = perm.rsplit('_', 2)
            content_type = ContentType.objects.get(
                app_label=app_label, model=model)
            permission = Permission.objects.get(
                content_type=content_type, codename=f'{action}_{model}')
            group.permissions.add(permission)
        except ContentType.DoesNotExist:
            print(f"ContentType not found for {app_label}.{model}")
            continue
        except Permission.DoesNotExist:
            print(f"Permission not found: {perm}")
            continue

    # Remove old permissions
    for perm in permissions_to_remove:
        try:
            print("perm_to_remove: ", perm)
            action, model, app_label = perm.rsplit('_', 2)
            content_type = ContentType.objects.get(
                app_label=app_label, model=model)
            permission = Permission.objects.get(
                content_type=content_type, codename=f'{action}_{model}')
            group.permissions.remove(permission)
        except ContentType.DoesNotExist:
            print(f"ContentType not found for {app_label}.{model}")
            continue
        except Permission.DoesNotExist:
            print(f"Permission not found: {perm}")
            continue
    groups = Group.objects.all()

    permission_list = populate_groups_permissions(groups)
    context = {
        "groups_permissions": permission_list
    }

    return render(request, 'mgt/users/partials/groups-table.html', context)
