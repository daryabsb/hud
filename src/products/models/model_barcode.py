from django.db import models
from src.accounts.models import User

class Barcode(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="barcodes")
    product = models.OneToOneField(
        "Product", on_delete=models.CASCADE, related_name="barcode"
    )
    value = models.CharField(max_length=250, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.product.name}) - {self.value}"