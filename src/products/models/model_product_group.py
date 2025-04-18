from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from src.core.utils import slugify_function
from src.accounts.models import User
from src.core.modules import upload_image_file_path
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class ProductGroup(MPTTModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="productGroups"
    )
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', blank=False, unique=True,
                         slugify_function=slugify_function)
    parent = TreeForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="groups"
    )
    color = models.CharField(max_length=50, default="Transparent")
    image = models.ImageField(null=True, blank=True,
                              upload_to=upload_image_file_path)
    rank = models.SmallIntegerField(default=0)
    is_product = models.BooleanField(default=False)

    is_enabled = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        verbose_name = _('ProductGroup')
        verbose_name_plural = "ProductGroups"

    class Meta:
        ordering = ("rank",)
        verbose_name = "ProductGroup"
        verbose_name_plural = "ProductGroups"

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def has_children(self):
        return self.groups is not None
