from django.shortcuts import render
from django.contrib.auth.models import Group
from collections import defaultdict
from src.accounts.models import User
from src.management.utils import populate_users_permissions, populate_groups_permissions

list_permissions = [
    {
        'app': 'accounts',
        'models': ['user', 'company']
    },
    {
        'app': 'finances',
        'models': ['tax', 'pos_order']
    },
]


def mgt_users(request):
    users = User.objects.all()
    permission_list = populate_users_permissions(users)

    groups_list = Group.objects.all()
    lone_group = Group.objects.first()
    groups_permission_list = populate_groups_permissions(groups_list)

    permissions_by_app_model = defaultdict(lambda: defaultdict(list))

    context = {
        "users": users,
        "groups": groups_list,
        "permissions": permission_list,
        "groups_permissions": groups_permission_list,
        'permissions_by_app_model': dict(permissions_by_app_model),
        "list_permissions": list_permissions,
        # "users_with_permissions": users_with_permissions,
        # "groups_with_permissions": groups_with_permissions,
    }
    return render(request, 'mgt/users/list.html', context)