from django.db import models
from django.utils.text import slugify
from src.core.utils import slugify_function
from src.accounts.models import User
from src.core.modules import upload_image_file_path
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from colorfield.fields import ColorField


class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    # slug2 = models.SlugField(max_length=255, unique=True, null=True)
    slug = AutoSlugField(populate_from='name', blank=False, unique=True,
                         slugify_function=slugify_function)
    parent_group = TreeForeignKey(
        "ProductGroup", on_delete=models.CASCADE, related_name="products",
        default='products'
    )
    code = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    plu = models.IntegerField(null=True, blank=True)
    measurement_unit = models.CharField(
        max_length=10, null=True, blank=True, default='pcs')

    price = models.DecimalField(default=0.000, decimal_places=3, max_digits=11)
    currency = models.ForeignKey(
        "Currency", on_delete=models.CASCADE, related_name="products",
        null=True, blank=True, default=1
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
    color2 = models.CharField(max_length=50, default="Transparent")
    color = ColorField(default='#FFFFFF')
    is_enabled = models.BooleanField(default=True)
    age_restriction = models.SmallIntegerField(null=True, blank=True)
    last_purchase_price = models.DecimalField(
        default=0, decimal_places=3, max_digits=11)
    rank = models.SmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('parent_group__id',)  # 7822809558444

    def __str__(self):
        return self.name

    def img(self):
        from django.urls import reverse
        if self.image:
            return self.image.url
        elif self.parent_group.image:
            return self.parent_group.image.url
        return '/media/placeholder-image.jpg'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        rate = 0
        rate = rate / 100
        if self.price == 0 and self.margin is not None:
            markup = self.cost * self.margin / 100
            self.price = self.cost + markup
        else:
            delta = self.price - self.cost
            self.margin = delta / self.price * 100
        super(Product, self).save(*args, **kwargs)
