from collections import defaultdict
import ast
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from src.configurations.models import ApplicationProperty, ApplicationPropertySection
from src.configurations.forms import ConfigurationForm, ApplicationPropertyForm
from src.configurations.const import direct_save_fields, indirect_save_fields
# Create your views here.
from src.core.decorators import required_security_level
from src.core.utils import convert_value

# def convert_value(value):
#     try:
#         # Attempt to evaluate the value to its original type
#         return ast.literal_eval(value)
#     except (ValueError, SyntaxError):
#         # If evaluation fails, return the value as-is (it is a string)
#         return value


@required_security_level(3)
def settings_view(request):

    sections = ApplicationPropertySection.objects.prefetch_related(
        Prefetch('application_properties',
                 queryset=ApplicationProperty.objects.all())
    ).filter(parent__isnull=True)

    settings_list = []

    for section in sections:
        section_dict = {
            "name": section.name,
            "icon": section.icon,
            "description": section.description,
            "rows": [],
            "children": []
        }

        for prop in section.application_properties.all():
            form = ApplicationPropertyForm(instance=prop)
            section_dict["rows"].append({
                "form": form,
                "name": prop.name,
                "id": prop.id,
                "value": convert_value(prop.value),
                "title": prop.title,
                "description": prop.description,
                "input_type": prop.input_type,
                "editable": prop.editable,
                "order": prop.order,
                "params": prop.params,
                "created": prop.created,
                "updated": prop.updated,
            })

        for child in section.children.all():
            child_dict = {
                "name": child.name,
                "icon": child.icon,
                "rows": [],
                "children": []
            }

            for prop in child.application_properties.all():
                form = ApplicationPropertyForm(instance=prop)
                child_dict["rows"].append({
                    "form": form,
                    "name": prop.name,
                    "id": prop.id,
                    "value": convert_value(prop.value),
                    "title": prop.title,
                    "description": prop.description,
                    "input_type": prop.input_type,
                    "editable": prop.editable,
                    "order": prop.order,
                    "params": prop.params,
                    "created": prop.created,
                    "updated": prop.updated,
                })

            section_dict["children"].append(child_dict)

        settings_list.append(section_dict)

    context = {
        "page_title": "Settings",
        "sections": sections,
        "settings": settings_list,
    }

    return render(request, 'config/index.html', context)


def update_config(request, id):
    config = get_object_or_404(ApplicationProperty, id=id)

    if config.input_type in direct_save_fields:
        value = request.POST.get(f"{config.name}", '')
        if value:
            config.value = value
            config.save()

    elif config.input_type in indirect_save_fields:
        if config.input_type == 'checkbox' and config.params != '':
            value = request.POST.getlist(f"{config.name}", '')
            config.value = ','.join(value)
            config.save()
        elif config.input_type == 'checkbox' and config.params == '':
            value = request.POST.get(f"{config.name}", None)
            print("value = ", value)
            if value == 'on':
                config.value = 'True'
                config.save()
            else:
                config.value = 'False'
                config.save()
    # config.refresh_from_db()
    context = {
        "config": config
    }
    return render(request, 'config/partials/input_type.html', context)


'''
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from src.products.models import Product
from src.accounts.models import User

cash_group = Group.objects.get_or_create(name="Cashiers")

content_type = ContentType.objects.get_for_model(Product)

product_permission = Permission.objects.filter(content_type=content_type)

[perm.codename for perm in product_permission]
# ['add_product', 'change_product', 'delete_product', 'view_product']
user = User.objects.first()
user.groups.add(cash_group)

user = get_object_or_404(User, pk=user.id)

print(user.has_perm("products.add_product")) # => False
print(user.has_perm("products.change_product")) # => False
print(user.has_perm("products.delete_product")) # => True
print(user.has_perm("products.view_product")) # => True
'''
