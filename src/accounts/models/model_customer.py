from django.db import models
from src.accounts.models import User


class Customer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customers")
    code = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    # country = models.ForeignKey(
    #     "Country", default=1, on_delete=models.CASCADE, related_name="customers"
    # )
    tax_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_supplier = models.BooleanField(default=False)
    due_date_period = models.SmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} @ {self.city}"


class CustomerDiscount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_discounts"
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="discounts"
    )
    type = models.SmallIntegerField(default=0)
    uid = models.SmallIntegerField(default=0)
    value = models.FloatField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "type", "uid"], name="unique_customer_discounts"
            )
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.type} | {self.uid}"
