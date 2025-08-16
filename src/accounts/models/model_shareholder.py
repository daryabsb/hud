from django.db import models
from src.accounts.models import User, Company, Store



class ShareHolder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shareholders")
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shareholder")
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name="shareholders"
    )
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, 

        null=True, blank=True, related_name="shareholders"
    )
    shares = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Shareholder: {self.account.email}"
    
    
    karti nishimani hardukman hardu diwaka u karti zanyari