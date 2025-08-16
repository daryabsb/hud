
from django.db import models

class Warehouse(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="warehouses"
    )
    store = models.ForeignKey(
        "Store", on_delete=models.CASCADE, to_field="number", related_name="warehouses"
    )
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name