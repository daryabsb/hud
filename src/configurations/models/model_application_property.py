from django.db import models
from src.accounts.models import User

# Create your models here.


class ApplicationProperty(models.Model):
    INPUT_TYPE_CHOICES = (
        ('', 'Select InputType'),
        ('text', 'text'),
        ('textarea', 'textarea'),
        ('file', 'file'),
        ('checkbox', 'checkbox'),
        ('radio', 'radio'),
        ('button', 'button'),
        ('select', 'select'),
    )
    user = models.SmallIntegerField(default=1)
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="application_properties"
    # )
    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)
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
