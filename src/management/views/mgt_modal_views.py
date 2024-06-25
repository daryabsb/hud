from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.accounts.models import User

@login_required
@require_GET
def modal_add_group(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'mgt/modals/add-group-modal.html', context)


@login_required
@require_GET
def modal_add_user(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'mgt/modals/add-user-modal.html', context)