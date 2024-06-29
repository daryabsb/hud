from django.db import models
from src.accounts.models import User
from src.products.models import Product


class ProductPrintStation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_print_stations"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_print_stations"
    )
    print_station = models.ForeignKey(
        "PrintStation", on_delete=models.CASCADE, related_name="product_print_stations"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("product", "print_station"), name="product_print_station"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.print_station.name}"
