from django.db import models
from src.accounts.models import User

def get_tree_nodes_from_db(user_id=None):
    from django.forms.models import model_to_dict
    from src.finances.api.serializers import PaymentTypeSerializer
    queryset = PaymentType.objects.all()

    if user_id:
        queryset = queryset.filter(user__id=user_id)

    tree_data = [
        PaymentTypeSerializer(payment_type).data
        for payment_type in queryset]
    return tree_data

def get_tree_nodes(user_id=None, refresh=False, no_check=False):
    from django.core.cache import cache
    from src.finances.const import payment_type_cache_nodes
    cache_tree_name = payment_type_cache_nodes
    tree_data = cache.get(cache_tree_name)
    cache_timeout = 604800
    if tree_data is None or refresh:
        tree_data = get_tree_nodes_from_db()
        cache.set(cache_tree_name, tree_data, cache_timeout)
    else:
        tree_data = cache.get(cache_tree_name)
    return tree_data

class PaymentType(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_types"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True, blank=True)

    is_customer_required = models.BooleanField(default=False)
    is_fiscal = models.BooleanField(default=False)
    is_slip_required = models.BooleanField(default=False)
    is_change_allowed = models.BooleanField(default=True)
    ordinal = models.SmallIntegerField(unique=True)
    is_enabled = models.BooleanField(default=True)
    is_quick_payment = models.BooleanField(default=True)
    open_cash_drawer = models.BooleanField(default=False)
    shortcut = models.CharField(max_length=30, null=True, blank=True)
    mark_as_paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ordinal}: {self.name}"

    class Meta:
        ordering = ('ordinal',)

    def update_tree_nodes(self):
        get_tree_nodes(refresh=True)