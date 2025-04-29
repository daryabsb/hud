from django.db import models
from src.accounts.models import User, Warehouse, Customer
from src.products.models import Product

from src.core.utils import generate_cache_key

from django.core.cache import cache
from src.products.models import Product



CACHE_TIMEOUT = 604800  # 1 week

def get_stocks_from_db(user=None, warehouse=None, customer=None):
    from src.stock.api.serializers import StockSerializer
    queryset = Stock.objects.all()

    if user and not (user.is_staff or user.is_superuser):
        queryset = queryset.filter(user=user)

    if warehouse:
        queryset = queryset.filter(warehouse=warehouse)

    # if customer:
    #     queryset = queryset.filter(customer=customer)

    serializer = StockSerializer(queryset, many=True)
    return serializer.data  # This should be a list of dicts


def get_stocks(refresh=False, user=None, warehouse=None, customer=None):
    cache_key = generate_cache_key("stocks_list", user, warehouse, customer)

    if refresh:
        stocks = get_stocks_from_db(user, warehouse, customer)
        cache.set(cache_key, stocks, CACHE_TIMEOUT)
    else:
        stocks = cache.get(cache_key)        
        if stocks is None:
            stocks = get_stocks_from_db(user, warehouse, customer)
            cache.set(cache_key, stocks, CACHE_TIMEOUT)

    return stocks



def refresh_order_cache(user=None, warehouse=None, customer=None):
    """Manually refresh the order cache."""
    cache_key = generate_cache_key("order_list", user, warehouse, customer)
    orders = get_orders_from_db(user, warehouse, customer)
    cache.set(cache_key, orders, CACHE_TIMEOUT)

class Stock(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stocks",
        default=1)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stocks"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="stocks"
    )
    quantity = models.SmallIntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # unique_together = ('product', 'tax',)
        constraints = [
            models.UniqueConstraint(
                fields=["product", "warehouse"], name="unique_product_warehouses"
            )
        ]

    def __str__(self):
        return f"{self.quantity}{self.product.measurement_unit} of {self.product} @ {self.warehouse}"

    def save(self, *args, **kwargs):
        # if not self.pk:  # If the object is being created
        super().save(*args, **kwargs)
        self.refresh_cache

    def refresh_cache(self):
        refresh_order_cache(user=self.user, warehouse=self.warehouse)