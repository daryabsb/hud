from django.db import models
from src.accounts.models import User
from src.products.models import Product
from django.db.models import F, Sum, Case, When, Value
from decimal import Decimal


class PosOrderItem(models.Model):
    number = models.CharField(
        max_length=100, primary_key=True, db_index=True, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order_items"
    )
    order = models.ForeignKey(
        "PosOrder", on_delete=models.CASCADE, null=True, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="order_items"
    )
    round_number = models.DecimalField(
        decimal_places=3, max_digits=4, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=3,  max_digits=15, default=0)

    is_locked = models.BooleanField(default=False)
    discount = models.FloatField(default=0)
    discount_type = models.FloatField(default=0)

    discounted_amount = models.GeneratedField(
        expression=Case(
            When(discount_type=1, then=F('price') *
                 F('quantity') * (F('discount') / 100)),
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

    item_total = models.GeneratedField(
        expression=Case(
            When(discount_type=1, then=F('price') * F('quantity') -
                 F('price') * F('quantity') * (F('discount') / 100)),
            When(discount_type=0, then=F('price')
                 * F('quantity') - F('discount')),
            default=Value(0),
            output_field=models.DecimalField(
                decimal_places=3,  max_digits=15, default=0)
        ),
        output_field=models.DecimalField(
            decimal_places=3,  max_digits=15, default=0),
        db_persist=True
    )

    is_featured = models.BooleanField(default=False)
    # voide by = not comparable
    voided_by = models.SmallIntegerField(default=0)
    comment = models.TextField(null=True, blank=True)
    bundle = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}: {self.quantity}{self.product.measurement_unit}"

    def save(self, *args, **kwargs):
        import random
        from datetime import date
        if not self.number:
            min = 100
            max = 3999
            digits = str(random.randint(min, max))
            digits = (len(str(max))-len(digits))*'0'+digits
            target = 'item'
            print(digits)
            if target:
                self.number = f'{target}-{self.user.id}-{date.today().strftime("%d%m%Y")}-01-{digits}'
                
        self.order.update_items_subtotal()

        super(PosOrderItem, self).save(*args, **kwargs)
