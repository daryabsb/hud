from django.db import models
# from src.accounts.models import User

# Create your models here.


class SecurityKey(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="security_keys"
    )
    name = models.CharField(max_length=100, primary_key=True)
    level = models.SmallIntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: Level {self.level}"
