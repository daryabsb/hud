from django.db import models
from src.accounts.models import User
from src.products.models import Product


class Tax(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="taxes")
    name = models.CharField(max_length=30)
    rate = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    code = models.CharField(max_length=100, null=True, blank=True)
    is_fixed = models.BooleanField(default=False)
    is_tax_on_total = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    amount = models.FloatField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} @ {self.rate}"


class ProductTax(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="productTaxes"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="productTaxes"
    )
    tax = models.ForeignKey(
        "Tax", on_delete=models.CASCADE, related_name="productTaxes"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # unique_together = ('product', 'tax',)
        constraints = [
            models.UniqueConstraint(
                fields=["product", "tax"], name="unique_product_taxes"
            )
        ]

    def __str__(self):
        return f"{self.product.name} @ {self.tax.rate}"