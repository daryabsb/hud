from django.db import models
from src.accounts.models import User

# Create your models here.


class ApplicationProperty(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="application_properties"
    )
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name