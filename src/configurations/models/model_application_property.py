from django.db import models
from src.accounts.models import User
from fontawesome_5.fields import IconField
from src.core.utils import generate_cache_key
from src.configurations import cache_key as ck
from src.core.utils import recursive_to_dict

from django.core.cache import cache

# Create your models here.

CACHE_TIMEOUT = 604800  # 1 week


def get_props_from_db(user=None):
    from src.configurations.api.serializers import ApplicationPropertySerializer
    print("3 - Cache miss, fetching from DB")
    queryset = ApplicationProperty.objects.select_related('section')

    if user and not (user.is_staff or user.is_superuser):
        queryset = queryset.filter(user=user)

    serializer = ApplicationPropertySerializer(queryset, many=True)
    # This should be a list of dicts
    return [recursive_to_dict(item) for item in serializer.data]


def get_props(refresh=False, user=None):
    cache_key = ck.APPLICATION_PROPERTIES_CACHE_KEY % user

    if refresh:
        props = get_props_from_db(user)
        cache.set(cache_key, props, CACHE_TIMEOUT)
    else:
        props = cache.get(cache_key)
        if props is None:
            props = get_props_from_db(user)
            cache.set(cache_key, props, CACHE_TIMEOUT)
    return props

def refresh_props_cache(user=None):
    """Manually refresh the order cache."""
    cache_key = generate_cache_key("props_list", user)
    props = get_props_from_db(user)
    cache.set(cache_key, props, CACHE_TIMEOUT)

def get_menus(user=None, warehouse=None, customer=None):
    return [prop for prop in get_props(user=user) if prop["section"] == 'menu']

def get_layout(user=None):
    return [prop for prop in get_props(user=user) if prop["name"] == 'layout']

def get_prop(name, user=None ):
    return [prop for prop in get_props(user=user) if prop["name"] == name][0]
    

class ApplicationPropertySection(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children')
    name = models.CharField(max_length=50, unique=True)
    icon = IconField()
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ApplicationProperty(models.Model):
    INPUT_TYPE_CHOICES = (
        ('', 'Select InputType'),
        ('text', 'text'),
        ('number', 'number'),
        ('textarea', 'textarea'),
        ('file', 'file'),
        ('checkbox', 'checkbox'),
        ('radio', 'radio'),
        ('button', 'button'),
        ('select', 'select'),
    )
    user = models.SmallIntegerField(default=1)

    section = models.ForeignKey(
        "ApplicationPropertySection", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="application_properties"
    )
    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    input_type = models.CharField(
        max_length=255, choices=INPUT_TYPE_CHOICES, default=INPUT_TYPE_CHOICES[0][0])
    editable = models.BooleanField(default=True)
    order = models.IntegerField(null=True, blank=True)
    params = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


'''
from src.configurations.models import ApplicationProperty as ap
p = ap.objects.create(name='Theme.color',value='info')
'''

