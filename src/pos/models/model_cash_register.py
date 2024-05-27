from django.db import models

# MACHINE ID WILL BE THE ID FOR THE CASH REGISTER


class CashRegister(models.Model):
    number = models.CharField(
        max_length=100, primary_key=True, db_index=True, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
