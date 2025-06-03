from django.db import models
from src.accounts.models import User
from src.orders import cache_key as ck
from django.core.cache import cache

CACHE_TIMEOUT = 604800  # 1 week

def get_order_statuses_from_db(user=None):
    statuses = PosOrderStatus.objects.only('ordinal','name','color_class').order_by('ordinal')
    
    statuses_list = []
    for status in statuses:
        status_data = {   
        "ordinal": status.ordinal,
        "name": status.name,
        "color_class": str(status.color_class),
        }
        statuses_list.append(status_data)
    return statuses_list

def get_order_statuses(user, refresh=False):
    if user and not (user.is_staff or user.is_superuser):
        cache_key = ck.USER_ORDER_STATUSES_CACHE_KEY % user.id # generate_cache_key("order_statuses_list", user, warehouse, customer)
    else:
        cache_key = ck.ORDER_STATUSES_LIST_CACHE_KEY # generate_cache_key("order_statuses_list", user, warehouse, customer)
    if refresh:
        print(f"1 - Cache miss, fetching from DB - refresh: {refresh}")
        order_statuses = get_order_statuses_from_db(user)
        cache.set(cache_key, order_statuses, CACHE_TIMEOUT)
    else:
        order_statuses = cache.get(cache_key)
        # print(f"Cache key: {cache_key}")
        # print(f"Cache value: {order_statuses}")

        if order_statuses is None:
            print("2 - Cache miss, fetching order_statuses DB")
            order_statuses = get_order_statuses_from_db(user)
            cache.set(cache_key, order_statuses, CACHE_TIMEOUT)

    return order_statuses


def refresh_order_statuses_cache(user=None):
    """Manually refresh the order cache."""
    if user and not (user.is_staff or user.is_superuser):
        cache_key = ck.USER_ORDER_STATUSES_CACHE_KEY % user.id # generate_cache_key("orders_list", user, warehouse, customer)
    else:
        cache_key = ck.ORDER_STATUSES_LIST_CACHE_KEY
    order_statuses = get_order_statuses_from_db(user)
    cache.set(cache_key, order_statuses, CACHE_TIMEOUT)

class PosOrderStatus(models.Model):
    class ColorClassChoices(models.TextChoices):
        WARNING = 'warning', 'border-warning text-warning'  # Unfulfilled
        INFO = 'info', 'border-info text-info',       # Ready for pickup
        PRIMARY = 'primary', 'border-primary text-primary',  # Ready for delivery
        DANGER = 'danger', 'border-danger text-danger',  # Cancelled
        SUCCESS = 'success', 'border-success text-success',  # Fulfilled
        # DEFAULT = 'default', 'border-default text-default',  # Fulfilled
        DEFAULT = 'default', 'btn-outline-default text-default',  # Fulfilled
        
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order_statuses"
    )
    name = models.CharField(max_length=55)
    ordinal = models.SmallIntegerField(unique=True)
    color_class = models.CharField(max_length=55, choices=ColorClassChoices.choices,
                            default=ColorClassChoices.DEFAULT)
    
    def __str__(self):
        return f'{self.ordinal} - {self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_cache()

    def refresh_cache(self):
        refresh_order_statuses_cache(user=self.user)

    class Meta:
        ordering = ['ordinal']