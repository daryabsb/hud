

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group
from src.products.models import ProductGroup
from src.products.forms import (
    ProductGroupForm, ConfirmPasswordForm
)


@require_POST
@login_required
def update_product_group(request, slug=None):
    group = None
    if slug:
        group = get_object_or_404(ProductGroup, slug=slug)
    form = ProductGroupForm(request.POST, instance=group)

    if form.is_valid():
        group = form.save(commit=False)
        group.user = request.user
        print("slug is: ", group.slug)
        group.save()
    groups_list = Group.objects.all()
    context = {
        "groups": groups_list,
    }

    return render(request, 'mgt/products/partials/sidebar.html', context)


@require_POST
@login_required
def add_product_group(request):

    group_id = request.POST.get('group-id', None)
    if group_id:
        print("group id from update is: ", group_id)
        group = get_object_or_404(ProductGroup, id=group_id)
        form = ProductGroupForm(request.POST, instance=group)
    else:
        form = ProductGroupForm(request.POST)

    if form.is_valid():
        group = form.save(commit=False)
        group.user = request.user
        group.save()
    groups_list = ProductGroup.objects.all()
    context = {
        "groups": groups_list,
    }

    return render(request, 'mgt/products/partials/sidebar.html', context)


def delete_product_group(request):
    from django.contrib.auth import authenticate
    group_id = request.POST.get('delete-group-id', None)
    form = ConfirmPasswordForm(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user is not None:
            group = get_object_or_404(ProductGroup, id=group_id)
            group.delete()
            groups_list = ProductGroup.objects.all()
            context = {
                "groups": groups_list,
            }
            return render(request, 'mgt/products/partials/sidebar.html', context)

    # group.delete()