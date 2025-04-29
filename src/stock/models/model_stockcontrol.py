
from django.db import models
from src.accounts.models import User, Customer
from src.products.models import Product

class StockControl(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stock_controls"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_controls"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True,
        related_name="stock_controls", default=1
    )
    reorder_point = models.FloatField(default=0)
    preferred_quantity = models.SmallIntegerField(default=1)
    is_low_stock_warning_enabled = models.BooleanField(default=True)
    low_stock_warning_quantity = models.SmallIntegerField(default=1)

    class Meta:
        indexes = [models.Index(
            fields=["product"], name="stock_control_product_index")]
