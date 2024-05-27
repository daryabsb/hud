from django.db import models
from src.accounts.models import User
from src.documents.models import Document


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments")
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        related_name="payments",
    )
    payment_type = models.ForeignKey(
        "PaymentType", on_delete=models.DO_NOTHING, related_name="payments"
    )
    amount = models.FloatField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document:{self.document}= Amount ({self.amount})"

    class Meta:
        ordering = ['document']
