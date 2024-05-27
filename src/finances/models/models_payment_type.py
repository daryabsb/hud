from django.db import models
from src.accounts.models import User


class PaymentType(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_types"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True, blank=True)

    is_customer_required = models.BooleanField(default=False)
    is_fiscal = models.BooleanField(default=False)
    is_slip_required = models.BooleanField(default=False)
    is_change_allowed = models.BooleanField(default=True)
    ordinal = models.SmallIntegerField(unique=True)
    is_enabled = models.BooleanField(default=True)
    is_quick_payment = models.BooleanField(default=True)
    open_cash_drawer = models.BooleanField(default=False)
    shortcut = models.CharField(max_length=30, null=True, blank=True)
    mark_as_paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ordinal}: {self.name}"

    class Meta:
        ordering = ('ordinal',)
