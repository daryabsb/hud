from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.accounts.models import User
from src.products.forms import ProductGroupForm
from src.products.models import ProductGroup


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


@login_required
@require_GET
def modal_add_product(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'mgt/modals/add-product-modal.html', context)


@login_required
@require_GET
def modal_add_product(request):
    group = None
    users = User.objects.all()
    group_id = request.GET.get('group-id', None)

    print("group_id = ", group_id)

    if group_id:
        group = get_object_or_404(ProductGroup, id=group_id)
        form = ProductGroupForm(instance=group)
        context = {"group": group, "form": form}
        return render(request, 'mgt/modals/add-product-group-modal.html', context)
    return render(request, 'mgt/modals/add-product-group-modal.html', {"form": form})
