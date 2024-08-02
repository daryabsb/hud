from django import template
from django.apps import apps
import json


register = template.Library()

app_name = 'products'
model_name = 'Product'


def format_title(field_name):
    """Format the field name into a more readable title."""
    return ' '.join(word.capitalize() for word in field_name.split('_'))


@register.filter(name='get_columns')
def get_columns(app_name, model_name):
    from src.core.utils import get_columns as gc
    return json.dumps(gc(app_name))
