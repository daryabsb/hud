# myapp/templatetags/custom_tags.py
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def length(list):
    return len(list)
