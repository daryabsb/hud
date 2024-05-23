from django.db import models
from django.utils.text import slugify
from src.accounts.models import User
from src.core.modules import upload_image_file_path
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class ProductGroup(MPTTModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="productGroups"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="groups"
    )
    color = models.CharField(max_length=50, default="Transparent")
    image = models.ImageField(null=True, blank=True,
                              upload_to=upload_image_file_path)
    rank = models.SmallIntegerField(default=0)
    is_product = models.BooleanField(default=False)

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
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def has_children(self):
        return self.groups is not None
