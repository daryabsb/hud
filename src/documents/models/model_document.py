from django.db import models
from src.accounts.models import User, Warehouse, Customer
from src.pos.models import CashRegister
# from src.orders.models import PosOrder
from datetime import datetime, timedelta
from src.documents.managers import DocumentManager

today = datetime.now()
due_date = today + timedelta(days=15)
def get_due_date():
    return 15

TRUE_FALSE_CHOICES = (
    (True, 'Paid'),
    (False, 'Unpaid')
)


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
    order = models.CharField(max_length=50, null=True, blank=True)

    document_type = models.ForeignKey(
        "DocumentType", on_delete=models.DO_NOTHING, related_name="documents"
    )
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.DO_NOTHING,
        related_name="documents"
    )
    date = models.DateTimeField(null=True, blank=True)
    reference_document_number = models.CharField(max_length=100, unique=True)
    internal_note = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    due_date = models.SmallIntegerField(default=get_due_date)
    discount = models.SmallIntegerField(default=0)
    discount_type = models.SmallIntegerField(default=0)
    discount_apply_rule = models.SmallIntegerField(default=0)
    paid_status = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES)
    stock_date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0)
    is_clocked_out = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = DocumentManager()

    def __str__(self):
        return f"{self.document_type.stock_direction} | {self.total}  | {self.number} | Pay status: {'Paid' if self.paid_status else 'Not Paid'}"
