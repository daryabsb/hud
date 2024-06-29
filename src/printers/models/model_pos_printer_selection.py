from django.db import models
from src.accounts.models import User
from src.pos.models import CashRegister

# Create your models here.


class PosPrinterSelection(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Pos_printer_selections"
    )
    key = models.CharField(max_length=30, unique=True)
    cash_register = models.ForeignKey(
        CashRegister, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="Pos_printer_selections"
    )
    printer_name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # ADD CASH REGISTER KEY AS UNIQUE TOGETHER WITH KEY
                fields=["key", "cash_register"], name="unique_printer_keys")
        ]

    def __str__(self):
        return f"{self.printer_name}: {self.key}" \
            + f"| IsEnabled= {self.is_enabled}"
