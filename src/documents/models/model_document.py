from django.db import models
from src.accounts.models import User, Warehouse, Customer
from src.pos.models import CashRegister
from src.orders.models import PosOrder


class Document(models.Model):
    number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="documents")
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING,
        null=True, blank=True, related_name="documents"
    )
    cash_register = models.ForeignKey(
        CashRegister, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="documents"
    )
    order = models.ForeignKey(
        PosOrder, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="documents")
    document_type = models.ForeignKey(
        "DocumentType", on_delete=models.DO_NOTHING, related_name="documents"
    )
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.DO_NOTHING,
        related_name="documents"
    )
    date = models.DateTimeField(auto_now_add=True)
    reference_document_number = models.CharField(max_length=100, unique=True)
    internal_note = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(auto_now_add=True)
    discount = models.SmallIntegerField(default=0)
    discount_type = models.SmallIntegerField(default=0)
    discount_apply_rule = models.SmallIntegerField(default=0)
    paid_status = models.BooleanField(default=False)
    stock_date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0)
    is_clocked_out = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.language}: {self.name}"
