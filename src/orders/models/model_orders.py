from django.db import models
from src.accounts.models import User, Customer, Warehouse
from src.core.utils import generate_number
from django.db.models import F, Sum, Case, When, Value
from src.documents.models import DocumentType
from src.orders.const import ORDER_STATUS
from src.core.utils import generate_cache_key
from src.orders import cache_key as ck
from django.core.cache import cache
from src.products.models import Product

from src.core.utils import recursive_to_dict

CACHE_TIMEOUT = 604800  # 1 week


def get_orders_from_db(user=None, warehouse=None, customer=None):
    from src.orders.api.serializers import PosOrderSerializer
    from src.orders.utils import _get_orders_from_db
    print("3 - Cache miss, fetching from DB")
    orders = _get_orders_from_db()
    # This should be a list of dicts
    return orders


def get_orders(user=None, warehouse=None, customer=None, refresh=False):
    if user and not (user.is_staff or user.is_superuser):
        cache_key = ck.USER_ORDERS_CACHE_KEY % user.id # generate_cache_key("orders_list", user, warehouse, customer)
    else:
        cache_key = ck.ORDERS_LIST_CACHE_KEY # generate_cache_key("orders_list", user, warehouse, customer)
    
    if refresh:
        print(f"1 - Cache miss, fetching from DB - refresh: {refresh}")
        orders = get_orders_from_db(user, warehouse, customer)
        cache.set(cache_key, orders, CACHE_TIMEOUT)
    else:
        orders = cache.get(cache_key)
        # print(f"Cache key: {cache_key}")
        # print(f"Cache value: {orders}")

        if orders is None:
            print("2 - Cache miss, fetching orders DB")
            orders = get_orders_from_db(user, warehouse, customer)
            cache.set(cache_key, orders, CACHE_TIMEOUT)

    return orders


def refresh_order_cache(user=None, warehouse=None, customer=None):
    """Manually refresh the order cache."""
    if user and not (user.is_staff or user.is_superuser):
        cache_key = ck.USER_ORDERS_CACHE_KEY % user.id # generate_cache_key("orders_list", user, warehouse, customer)
    else:
        cache_key = ck.ORDERS_LIST_CACHE_KEY
    orders = get_orders_from_db(user, warehouse, customer)
    cache.set(cache_key, orders, CACHE_TIMEOUT)


class PosOrder(models.Model):

    number = models.CharField(
        max_length=100, primary_key=True, db_index=True, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders",
        null=True, blank=True, default=1)
    item_subtotal = models.DecimalField(
        decimal_places=3,  max_digits=15, default=0)
    # total_tax_payer = models.DecimalField(
    #     decimal_places=3,  max_digits=15, default=0)
    # total_tax = models.DecimalField(
    #     decimal_places=3,  max_digits=15, default=0)
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.DO_NOTHING,
        related_name="orders", default=1
    )
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.DO_NOTHING,
        related_name="orders", default=1
    )
    date = models.DateTimeField(auto_now_add=True)
    reference_document_number = models.CharField(
        max_length=100, null=True, blank=True,)
    internal_note = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(auto_now_add=True)

    discount = models.FloatField(default=0)
    discount_type = models.FloatField(default=0)
    discounted_amount = models.GeneratedField(
        expression=Case(
            When(discount_type=1, then=F('item_subtotal')
                 * (F('discount') / 100)),
            When(discount_type=0, then=F('discount')),
            default=Value(0),
            output_field=models.DecimalField(
                decimal_places=3,  max_digits=15, default=0)
        ),
        output_field=models.DecimalField(decimal_places=3,  max_digits=15, default=0), db_persist=True,)
    discount_sign = models.GeneratedField(
        expression=Case(
            When(discount_type=1, then=Value('%')),
            When(discount_type=0, then=Value('$')),
            default=Value(''),
            output_field=models.CharField(max_length=20)
        ),
        output_field=models.CharField(max_length=20), db_persist=False,)

    subtotal_after_discount = models.GeneratedField(
        expression=F('item_subtotal') - F('discounted_amount'),
        output_field=models.DecimalField(
            decimal_places=3,  max_digits=15, default=0),
        db_persist=False)

    fixed_taxes = models.DecimalField(
        decimal_places=3,  max_digits=15, default=0)

    total_tax_rate = models.DecimalField(
        decimal_places=3,  max_digits=15, default=0)

    total_tax = models.GeneratedField(
        expression=F('fixed_taxes') + F('subtotal_after_discount') *
        F('total_tax_rate') / 100,
        output_field=models.DecimalField(
            decimal_places=3,  max_digits=15, default=0),
        db_persist=False)

    total = models.GeneratedField(
        expression=F('subtotal_after_discount') + F('total_tax'),
        output_field=models.DecimalField(
            decimal_places=3,  max_digits=15, default=0),
        db_persist=False)

    paid_status = models.BooleanField(default=False)
    status = models.IntegerField(
        choices=ORDER_STATUS,
        default=1,  # Default to 'Unfulfilled'
        help_text="Current status of the order"
    )
    is_active = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # objects = OrderManager()
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.number}: {self.total}"

    def save(self, *args, **kwargs):
        # if not self.pk:  # If the object is being created

        if self.number is None or self.number == '':
            doc_type = kwargs.pop('doc_type', 'order')
            self.number = generate_number(doc_type)
        self.set_tax_fields()
        super().save(*args, **kwargs)
        self.refresh_cache

    def refresh_cache(self):
        refresh_order_cache(
            user=self.user, warehouse=self.warehouse, customer=self.customer)

    def get_status_class(self):
        status_classes = {
            1: 'border-warning text-warning',  # Unfulfilled
            2: 'border-info text-info',       # Ready for pickup
            3: 'border-primary text-primary',  # Ready for delivery
            4: 'border-danger text-danger',  # Cancelled
            5: 'border-success text-success',  # Fulfilled
        }
        return status_classes.get(self.status, '')

    def set_tax_fields(self):
        # Calculate fixed taxes and total tax rate
        from src.tax.models import Tax
        from decimal import Decimal
        taxes = Tax.objects.filter(is_tax_on_total=True).aggregate(
            fixed_tax=Sum(Case(
                When(is_fixed=True, then=F('amount')),
                default=Value(0),
                output_field=models.DecimalField(
                    decimal_places=3,  max_digits=15, default=0)
            )),
            percentage_tax=Sum(Case(
                When(is_fixed=False, then=F('rate')),
                default=Value(0),
                output_field=models.DecimalField(
                    decimal_places=3,  max_digits=15, default=0)
            ))
        )

        self.fixed_taxes = taxes['fixed_tax'] or Decimal('0.00')
        self.total_tax_rate = taxes['percentage_tax'] or Decimal('0.00')

    def update_items_subtotal(self):
        # Calculate the subtotal based on order items

        self.item_subtotal = sum(item.item_total for item in self.items.all())

        # customer_discounts = self.customer.discounts.all()
        # for discount in customer_discounts:
        #     if discount.type == 1:  # Percentage discount
        #         self.item_subtotal -= (discount.value / 100) * \
        #             self.item_subtotal
        #     else:  # Fixed amount discount
        #         self.item_subtotal -= discount.value

        self.save()

    @property
    def currency(self):
        if self.items.exists():
            return self.items.first().product.currency.name
        return ""

    @property
    def subtotal(self):
        return self.items.aggregate(
            total=Sum(F('price') * F('quantity')))['total'] or 0
    # def __str__(self):
    #     return f"{self.number}:" + \
    #         f" [{self.total}]" + \
    #         f" ({'Completed' if self.status else 'Pending'})"
