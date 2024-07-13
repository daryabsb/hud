from django.db import models
from src.accounts.models import User, Company


class CompanyLetterhead(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="company_letterheads"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name="letterheads"
    )
    name = models.CharField(max_length=30, default='Company Letterhead')
    letterhead_options = models.ForeignKey("CompanyLetterheadOption",
                                           on_delete=models.CASCADE, related_name="options")
    is_default = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
