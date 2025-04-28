from django.db import models
from django.utils.text import slugify
from src.core.utils import slugify_function
from src.accounts.models import User, Country
from src.core.modules import upload_image_file_path
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from colorfield.fields import ColorField
from django_countries.fields import CountryField
from src.products.managers import ProductManager


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
    country_of_origin = models.CharField(
        max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Country')])
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
    # color2 = models.CharField(max_length=50, default="Transparent")
    color = ColorField(default='#FFFFFF')
    is_enabled = models.BooleanField(default=True)
    age_restriction = models.SmallIntegerField(null=True, blank=True)
    last_purchase_price = models.DecimalField(
        default=0, decimal_places=3, max_digits=11)
    rank = models.SmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

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

    @staticmethod
    def get_fields():
        """Returns a list of field names for the given app_name."""
        from src.configurations.models import AppTableColumn
        columns = AppTableColumn.objects.filter(
            app__name='products', searchable=True)
        return [
            column.related_value if column.is_related else column.name
            for column in columns
        ]

    @staticmethod
    def get_columns():
        """Returns a list of column configurations for the given app_name."""
        from src.configurations.models import AppTableColumn
        columns = AppTableColumn.objects.filter(
            app__name='products', searchable=True)
        return [
            {
                "id": index,
                "data": column.related_value if column.is_related else column.name,
                "name": column.name,
                "title": column.title,
                "searchable": column.searchable,
                "orderable": column.orderable,
            }
            for index, column in enumerate(columns)
        ]

    @staticmethod
    def get_indexes():
        """Returns a dictionary mapping column names to their indexes."""
        print('indees called')
        from src.configurations.models import AppTableColumn
        columns = AppTableColumn.objects.filter(
            app__name='products', searchable=True)
        indexes = {column.name: index for index, column in enumerate(columns)}
        indexes['start_date'] = len(indexes)
        indexes['end_date'] = len(indexes)
        return indexes

    @staticmethod
    def get_related_fields():
        """Returns a list of related fields for select_related."""
        return ['currency', 'barcode', 'parent_group', 'user']

    @staticmethod
    def get_annotations_fields():
        from django.db.models import Q, F
        """Returns a list of related fields for select_related."""
        return {
            'user__name': F('user__name'),
            'barcode__value': F('barcode__value'),
            'parent_group__name': F('parent_group__name'),
            'currency__name': F('currency__name'),
        }
