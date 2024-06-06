from collections import defaultdict
import ast
from django.db.models import Prefetch
from django.shortcuts import render
from src.configurations.models import ApplicationProperty, ApplicationPropertySection
from src.configurations.forms import ConfigurationForm
# Create your views here.


def convert_value(value):
    try:
        # Attempt to evaluate the value to its original type
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If evaluation fails, return the value as-is (it is a string)
        return value


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
            form = ConfigurationForm(instance=prop)
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
                form = ConfigurationForm(instance=prop)
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
