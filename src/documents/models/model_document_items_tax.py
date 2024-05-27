from django.db import models
from src.accounts.models import User
from src.tax.models import Tax


class DocumentItemTax(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="document_item_taxes"
    )
    document_item = models.ForeignKey(
        "DocumentItem",
        on_delete=models.CASCADE,
        null=True,
        related_name="document_item_taxes",
    )
    tax = models.ForeignKey(
        Tax, on_delete=models.DO_NOTHING, related_name="document_item_taxes"
    )
    amount = models.FloatField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DocItem ID:{self.document_item.id}= Amount ({self.amount})"
