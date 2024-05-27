from django.db import models
from src.accounts.models import User


class Counter(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="country")
    name = models.CharField(max_length=30)
    value = models.SmallIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
