from django.db import models
from src.accounts.models import User, Warehouse


class DocumentType(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="document_types"
    )
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50)
    category = models.ForeignKey(
        "DocumentCategory",
        on_delete=models.SET_NULL,
        null=True,
        related_name="document_types",
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL,
        null=True, related_name="document_types"
    )
    stock_direction = models.SmallIntegerField(default=0)
    editor_type = models.SmallIntegerField(default=0)
    print_template = models.TextField(null=True, blank=True)
    price_type = models.SmallIntegerField(default=0)
    language = models.CharField(max_length=4)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} | {self.name}"
