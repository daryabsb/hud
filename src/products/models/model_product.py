from django.db import models
from django.utils.text import slugify
from src.accounts.models import User
from src.core.modules import upload_image_file_path
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    parent_group = TreeForeignKey(
        "ProductGroup", on_delete=models.CASCADE, related_name="products"
    )
    code = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    plu = models.IntegerField(null=True, blank=True)
    measurement_unit = models.CharField(max_length=10, null=True, blank=True)

    price = models.DecimalField(default=3, decimal_places=3, max_digits=11)
    currency = models.ForeignKey(
        "Currency", on_delete=models.CASCADE, related_name="products"
    )
    is_tax_inclusive_price = models.BooleanField(default=False)
    is_price_change_allowed = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)
    is_using_default_quantity = models.BooleanField(default=True)
    is_product = models.BooleanField(default=True)
    cost = models.DecimalField(
        default=0, null=True, blank=True, decimal_places=3, max_digits=11)
    margin = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    image = models.ImageField(null=True, blank=True,
                            upload_to=upload_image_file_path)
    color = models.CharField(max_length=50, default="Transparent")
    is_enabled = models.BooleanField(default=True)
    age_restriction = models.SmallIntegerField(null=True, blank=True)
    last_purchase_price = models.DecimalField(
        default=0, decimal_places=3, max_digits=11)
    rank = models.SmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def img(self):
        from django.urls import reverse
        if self.image:
            return self.image.url
        return '/media/placeholder-image.jpg'

    def save(self, *args, **kwargs):
        rate = 0
        rate = rate / 100
        print('price: ', self.price)
        print('markup: ', self.margin)

        if self.price == 0 and self.margin is not None:
            markup = self.cost * self.margin / 100
            self.price = self.cost + markup
        else:
            delta = self.price - self.cost
            self.margin = delta / self.price * 100
        super(Product, self).save(*args, **kwargs)