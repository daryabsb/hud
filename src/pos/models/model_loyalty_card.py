from django.db import models
from src.accounts.models import User, Customer


class LoyaltyCard(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_loyalty_cards"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_loyalty_cards"
    )
    number = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta:
    #     indexes = [models.Index(fields=['customer']),]

    def __str__(self):
        return f"{self.customer.name} - {self.number}"
