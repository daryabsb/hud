from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.accounts.models import User
from src.products.forms import ProductGroupForm, ConfirmPasswordForm
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
def modal_update_product_group(request):
    group = None
    group_id = request.GET.get('group-id', None)
    parent_id = request.POST.get('parent-id', None)


    if group_id:
        group = get_object_or_404(ProductGroup, id=group_id)
        form = ProductGroupForm(instance=group)
        context = {"group": group, "form": form}
        return render(request, 'mgt/modals/add-product-group-modal.html', context)
    if parent_id:
        parent_group = get_object_or_404(ProductGroup, id=parent_id)
        form = ProductGroupForm(initial={'parent_group': parent_group})
    else:
        form = ProductGroupForm()
    return render(request, 'mgt/modals/add-product-group-modal.html', {"form": form})


@login_required
@require_GET
def modal_add_product_group(request):

    parent_id = request.GET.get('group-id', None)

    if parent_id:
        parent = get_object_or_404(ProductGroup, id=parent_id)
    else:
        parent = get_object_or_404(ProductGroup, slug='products')

    form = ProductGroupForm(initial={'parent': parent})
    return render(request, 'mgt/modals/add-product-group-modal.html', {"form": form})


@login_required
@require_GET
def modal_delete_product_group(request):
    group_id = request.GET.get('group-id', None)
    group = get_object_or_404(ProductGroup, id=group_id)
    print("group_delete = ", group.name)
    form = ConfirmPasswordForm()
    context = {"group": group, "form": form}
    return render(request, 'mgt/modals/confirm-test.html', context)
