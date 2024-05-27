from django.db import models
from src.accounts.models import User


class FloorPlan(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="floor_plans"
    )
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default="Transparent")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
