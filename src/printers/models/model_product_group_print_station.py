from django.db import models
from src.accounts.models import User
from src.products.models import ProductGroup


class ProductGroupPrintStation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_group_print_stations"
    )
    product_group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name="product_group_print_stations",
    )
    print_station = models.ForeignKey(
        "PrintStation",
        on_delete=models.CASCADE,
        related_name="product_group_print_stations",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("product_group", "print_station"), name="pg_print_station"
            )
        ]

    def __str__(self):
        return f"{self.product_group.name} - {self.print_station.name}"
