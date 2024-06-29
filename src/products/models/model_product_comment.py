from django.db import models
from src.accounts.models import User

class ProductComment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.CharField(max_length=300)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.created}"