from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from src.accounts.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


@login_required
@require_POST
def mgt_update_permissions(request):
    from src.management.utils import populate_users_permissions
    user_id = request.POST.get('user-id')
    new_permissions = request.POST.getlist('permissions')

    print("new_permissions = ", new_permissions)
    
    user = get_object_or_404(User, pk=user_id)
    
    # Extract the current permissions of the user
    current_permissions = user.user_permissions.all()
    print("current_permissions = ", current_permissions)
    
    # Create sets for easier comparison
    current_permission_codenames = set(
        f"{p.codename}_{p.content_type.app_label}" for p in current_permissions
    )
    new_permission_codenames = set(new_permissions)
    
    # Permissions to add
    permissions_to_add = new_permission_codenames - current_permission_codenames
    
    # Permissions to remove
    permissions_to_remove = current_permission_codenames - new_permission_codenames
    
    # Debug prints
    print("New permissions:", new_permissions)
    print("Current permissions:", current_permission_codenames)
    print("Permissions to add:", permissions_to_add)
    print("Permissions to remove:", permissions_to_remove)
    
    # Add new permissions
    for perm in permissions_to_add:
        try:
            action, model, app_label = perm.rsplit('_', 2)
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission = Permission.objects.get(content_type=content_type, codename=f'{action}_{model}')
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
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission = Permission.objects.get(content_type=content_type, codename=f'{action}_{model}')
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
    
    return JsonResponse({'status': 'success'})

list = [
    'view_user|False', 
    'add_company|False', 
    'view_company|False', 
    'change_tax|False', 
    'change_pos_order|False'
    ]
list = [
    'add_user|False', 
    'change_user|False', 
    'view_user|False', 
    'delete_user|False', 
    'add_company|False', 
    'view_company|False', 
    'delete_company|False', 
    'add_tax|False', 
    'view_tax|False', 
    'delete_tax|False', 
    'add_pos_order|False', 
    'change_pos_order|False', 
    'delete_pos_order|False'
    ]