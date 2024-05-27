from django.db import models
from src.accounts.models import User


class FloorPlanTable(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="floor_plan_tables"
    )
    name = models.CharField(max_length=100)
    floor_plan = models.ForeignKey(
        "FloorPlan", on_delete=models.CASCADE, related_name="tables"
    )
    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    is_round = models.SmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} @ {self.floor_plan.name}"
