from django.db import models
from src.pos.utils import get_computer_info
# MACHINE ID WILL BE THE ID FOR THE CASH REGISTER


class CashRegister(models.Model):
    number = models.CharField(
        max_length=100, primary_key=True,
        db_index=True, unique=True,
        default=get_computer_info()[1]
    )
    name = models.CharField(max_length=50, default=get_computer_info()[0])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
