from django.db import models
from src.accounts.models import User


class Currency(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="currencies"
    )
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=4)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}: {self.name}"
