from django.db import models
from src.accounts.models import User, Warehouse
from src.products.models import Product


class DocumentItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="document_items"
    )
    document = models.ForeignKey(
        "Document", on_delete=models.CASCADE, null=True, related_name="document_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="document_items"
    )
    quantity = models.SmallIntegerField(default=1)
    expected_quantity = models.SmallIntegerField(default=1)
    price_before_tax = models.FloatField(default=0)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    discount_type = models.FloatField(default=0)
    product_cost = models.FloatField(default=0)
    price_before_tax_after_discount = models.FloatField(default=0)
    price_after_descount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    total_after_document_discount = models.FloatField(default=0)
    discount_apply_rule = models.SmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}: {self.quantity} | total= {self.total}"
