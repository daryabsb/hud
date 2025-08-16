from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from src.accounts.models import User

class Account(models.Model):
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)  # e.g., "Savings", "Main", "Investment"
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.name} ({self.user.email}) - {self.balance}"


class Account2(models.Model):
    # Generic link to the "owner" of the account
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    owner = GenericForeignKey('content_type', 'object_id')

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.owner} - Balance: {self.balance}"

class CustomerAccountManager(models.Manager):
    def get_queryset(self):
        from django.contrib.contenttypes.models import ContentType
        customer_ct = ContentType.objects.get(app_label='your_app', model='customer')
        return super().get_queryset().filter(content_type=customer_ct)

class CustomerAccount(Account):
    objects = CustomerAccountManager()

    class Meta:
        proxy = True
        verbose_name = "Customer Account"
        verbose_name_plural = "Customer Accounts"
