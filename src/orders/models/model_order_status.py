from django.db import models
from src.accounts.models import User

def get_order_statuses_from_db(user=None):
    statuses = PosOrderStatus.objects.distinct(
        'name').only('ordinal','name','color_class')
    
    statuses_list = []
    for status in statuses:
        status_data = {   
        "ordinal": status.ordinal,
        "name": status.name,
        "color_class": str(status.get_status_display()),
        }
        statuses_list.append(status_data)
    return statuses_list

class PosOrderStatus(models.Model):
    class ColorClassChoices(models.TextChoices):
        WARNING = 'warning', 'border-warning text-warning'  # Unfulfilled
        INFO = 'info', 'border-info text-info',       # Ready for pickup
        PRIMARY = 'primary', 'border-primary text-primary',  # Ready for delivery
        DANGER = 'danger', 'border-danger text-danger',  # Cancelled
        SUCCESS = 'success', 'border-success text-success',  # Fulfilled
        DEFAULT = 'default', 'border-default text-default',  # Fulfilled
        
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order_statuses"
    )
    name = models.CharField(max_length=55)
    ordinal = models.SmallIntegerField(unique=True)
    color_class = models.CharField(max_length=55, choices=ColorClassChoices.choices,
                            default=ColorClassChoices.DEFAULT)
    
    def __str__(self):
        return f'{self.ordinal} - {self.name}'
    
    class Meta:
        ordering = ['ordinal']