from django.db import models
from src.accounts.managers import EmployeeManager


class Employee(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name='employee')
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = EmployeeManager()

    def __str__(self):
        return self.full_name