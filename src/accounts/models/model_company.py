
from django.db import models
from src.core.base import BaseNameModel, BaseModel, BaseAddress
from src.core.const import COMPANY_PREFIX
# delete_cache


# def get_tree_nodes_from_db(user=None, no_check=False):
#     """
#     Generate zTree data for companies
#     :return: List of dictionaries representing tree nodes
#     """
#     from django.apps import apps
#     from django.forms.models import model_to_dict
#     from src.companies.serializers import CompanySerializer
#     model_obj = apps.get_model('core', 'User')
#     usr_obj = isinstance(user, model_obj)

#     if usr_obj:
#         if user and not user.is_superuser:
#             queryset = user.companies.all()
#         else:
#             queryset = Company.objects.all()
#     else:
#         return []

#     tree_data = [
#            CompanySerializer(company).data
#         for company in queryset
#     ]
#     return tree_data


# def get_tree_nodes(user=None, refresh=False, no_check=False):
#     """
#     Cache tree data
#     :return:
#     """
#     from django.core.cache import cache
#     from django.apps import apps
#     model_obj = apps.get_model('core', 'User')
#     usr_obj = isinstance(user, model_obj)

#     if usr_obj:
#         if user and not user.is_representative:
#             cache_tree_name = 'companies_tree_nodes_' + str(user.id)
#         else:
#             cache_tree_name = 'companies_tree_nodes'
#     else:
#         cache_tree_name = 'companies_tree_nodes'

#     # Attempt to retrieve tree_data from the cache
#     tree_data = cache.get(cache_tree_name)
#     cache_timeout = 604800
#     if tree_data is None or refresh:
#         # If not found in cache or refresh flag is set, fetch data from the database
#         tree_data = get_tree_nodes_from_db(user, no_check)

#         # Cache the fetched data
#         cache.set(cache_tree_name, tree_data, cache_timeout)
#     return tree_data


class Company(BaseNameModel, BaseModel, BaseAddress):
    user = models.ForeignKey(
        "User", default=1, on_delete=models.CASCADE, related_name="companies"
    )
    code = models.CharField(unique=True, max_length=50)
    logo = models.OneToOneField(
        "Logo", on_delete=models.SET_NULL, null=True, blank=True, related_name="company"
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "companies"

    # def delete_cache(self):
    #     from src.client.global_cache import refresh_cache
    #     delete_cache(prefix=COMPANY_PREFIX, user=self.user, number=self.number)
    #     refresh_cache(self.user)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.handle:
            self.handle = slugify(self.name)
        super().save(*args, **kwargs)
        # self.delete_cache()

    # def delete(self, using=None, keep_parents=False):
    #     super().delete(using, keep_parents)
    #     self.delete_cache()

    def has_stores(self):
        return self.stores.exists()

    def items(self):
        return self.stores

    @property
    def logo_data(self):
        if self.logo is None:
            return {}
        return {
            "number": self.logo.number,
            "image": self.logo.image.url,
            "created": self.logo.created,
            "updated": self.logo.updated,
        }
