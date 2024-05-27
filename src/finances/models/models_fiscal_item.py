from django.db import models
from src.accounts.models import User


class FiscalItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fiscals")
    plu = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    vat = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.plu}"
