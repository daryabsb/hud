from collections import defaultdict
import ast
from django.shortcuts import render
from src.configurations.models import ApplicationProperty

# Create your views here.
def convert_value(value):
    try:
        # Attempt to evaluate the value to its original type
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If evaluation fails, return the value as-is (it is a string)
        return value

def settings_view(request):

    properties = ApplicationProperty.objects.all()
    sections_list = []
    settings_dict = defaultdict(lambda: {"name": "", "rows": []})

    for prop in properties:
        section, property_name = prop.name.split('.')

        
        if section not in settings_dict:
            settings_dict[section]["name"] = section
            sections_list.append(section)
        
        settings_dict[section]["rows"].append({
            "name": property_name,
            # "value": {
            "id": prop.id,
            "name": prop.name,
            "value": convert_value(prop.value),
            "title": prop.title,
            # "description": prop.description,
            # "input_type": prop.input_type,
            "editable": prop.editable,
            # "order": prop.order,
            # "params": prop.params,
            # "created": prop.created,
            # "updated": prop.updated
            # }
        })

    settings_list = list(settings_dict.values())
    context = {
        "page_title": "Settings",
        "sections": sections_list,
        "settings": settings_list,
    }

    return render(request, 'config/index.html', context)
