from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone
from pytz import UTC
import uuid as uuid_lib
from django.db import models
from django.urls import reverse
# import stripe

from .modules import upload_image_file_path
from django_countries.fields import CountryField


class BaseModel(models.Model):
    number = models.UUIDField(default=uuid_lib.uuid4,
                              primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseAddress(models.Model):
    tax_number = models.CharField(max_length=200, default="N/A")
    address = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=20, default='00000')
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, default="Iraq")
    street = models.CharField(max_length=350, null=True, blank=True)

    class Meta:
        abstract = True


class BaseNameModel(models.Model):
    name = models.CharField(max_length=200)
    handle = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def has_stores(self):
        return self.stores.exists()

    def get_absolute_url(self):
        return reverse(f"{self._meta.verbose_name_plural}:detail", kwargs={"handle": self.handle})

    def get_update_url(self):
        return reverse(f"{self._meta.verbose_name_plural}:update", kwargs={"handle": self.handle})

    @classmethod
    def get_create_url(cls):
        return reverse(f"{cls._meta.verbose_name_plural}:create", kwargs={})

    @property
    def display_name(self):
        return self.name


class PurchaseBase(models.Model):
    number = models.UUIDField(default=uuid_lib.uuid4,
                              primary_key=True, unique=True)
    user = models.ForeignKey("User",
                             default=1, on_delete=models.CASCADE, related_name='plan_purchases')

    stripe_checkout_session_id = models.CharField(
        max_length=220, null=True, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    completed = models.BooleanField(default=False)
    stripe_price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductBase(models.Model):
    number = models.UUIDField(default=uuid_lib.uuid4,
                              primary_key=True, unique=True)
    user = models.ForeignKey("User",
                             default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    handle = models.SlugField(unique=True)
    stripe_product_id = models.CharField(max_length=220, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    og_price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    stripe_price = models.IntegerField(default=0)
    stripe_price_id = models.CharField(max_length=220, null=True, blank=True)
    price_change_time = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to=upload_image_file_path)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        return self.name

    @property
    def display_price(self):
        return self.price

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.stripe_price and self.price is not None:
            self.stripe_price = int(self.price * 100)

        # if self.name:
        #     stripe_product_r = stripe.Product.create(name=self.name)
        #     self.stripe_product_id = stripe_product_r.id
        # if not self.stripe_price_id:
        #     stripe_price_obj = stripe.Price.create(
        #         product=self.stripe_product_id,
        #         unit_amount=self.stripe_price,
        #         currency="usd"
        #     )
        #     self.stripe_price_id = stripe_price_obj.id
        if self.price != self.og_price:
            # price changed
            self.og_price = self.price
            # trigger API request for the price
        self.stripe_price = int(self.price * 100)
        # if self.stripe_product_id:
        #     stripe_price_obj = stripe.Price.create(
        #         product=self.stripe_product_id,
        #         unit_amount=self.stripe_price,
        #         currency="usd"
        #     )
        # self.stripe_price_id = stripe_price_obj.id
        # self.price_change_time = timezone.now()
        super().save(*args, **kwargs)
        # self.update_tree_nodes()

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if self.name:
    #         stripe_product_r = stripe.Product.create(name=self.name)
    #         self.stripe_product_id = stripe_product_r.id
    #     if not self.stripe_price_id:
    #         stripe_price_obj = stripe.Price.create(
    #             product=self.stripe_product_id,
    #             unit_amount=self.stripe_price,
    #             currency="usd"
    #         )
    #         self.stripe_price_id = stripe_price_obj.id
    #     if self.price != self.og_price:
    #         # price changed
    #         self.og_price = self.price
    #         # trigger API request for the price
    #         self.stripe_price = int(self.price * 100)
    #         if self.stripe_product_id:
    #             stripe_price_obj = stripe.Price.create(
    #                 product=self.stripe_product_id,
    #                 unit_amount=self.stripe_price,
    #                 currency="usd"
    #             )
    #             self.stripe_price_id = stripe_price_obj.id
    #         self.price_change_time = datetime.now()
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"handle": self.handle})

    def get_manage_url(self):
        return reverse("products:manage", kwargs={"handle": self.handle})

    class Meta:
        abstract = True
