from django.db import models
from src.accounts.models import User
from fontawesome_5.fields import IconField

# Create your models here.


class ApplicationPropertySection(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children')
    name = models.CharField(max_length=50, unique=True)
    icon = IconField()

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
