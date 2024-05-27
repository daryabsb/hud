from django.db import models
from src.accounts.models import User


class DocumentCategory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="document_categories"
    )
    name = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=4)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.language}: {self.name}"
