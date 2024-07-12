from django.db import models
from src.accounts.models import User


class Region(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name


class Country(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="countries")
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=4)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
