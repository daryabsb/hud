from django.db import models
from src.core.base import BaseNameModel, BaseModel, BaseAddress
from src.core.const import STORE_PREFIX, delete_cache


# def get_tree_nodes_from_db(user=None, no_check=False):
#     """
#     Generate zTree data for companies
#     :return: List of dictionaries representing tree nodes
#     """
#     from django.apps import apps
#     from django.forms.models import model_to_dict
#     from src.stores.serializers import StoreForUserItemsSerializer
#     from src.subscriptions.serializers import UserplanForStoreSerializer
#     model_obj = apps.get_model('core', 'User')
#     usr_obj = isinstance(user, model_obj)

#     if usr_obj:
#         if user and not user.is_superuser:
#             queryset = user.stores.all()
#         else:
#             queryset = Store.objects.all()
#     else:
#         return []

#     tree_data = [ StoreForUserItemsSerializer(store).data for store in queryset]

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
#         if user and not user.is_superuser:
#             cache_tree_name = 'stores_tree_nodes_' + str(user.id)
#         else:
#             cache_tree_name = 'stores_tree_nodes'
#     else:
#         cache_tree_name = 'stores_tree_nodes'

#     # Attempt to retrieve tree_data from the cache
#     tree_data = cache.get(cache_tree_name)
#     cache_timeout = 604800
#     if tree_data is None or refresh:
#         # If not found in cache or refresh flag is set, fetch data from the database
#         tree_data = get_tree_nodes_from_db(user, no_check)

#         # Cache the fetched data
#         cache.set(cache_tree_name, tree_data, cache_timeout)

#     return tree_data


class Store(BaseNameModel, BaseModel, BaseAddress):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="stores")
    code = models.CharField(unique=True, max_length=50)
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, to_field="number", related_name="stores"
    )
    logo = models.OneToOneField(
        "Logo", on_delete=models.SET_NULL, null=True, blank=True, related_name="store"
    )
    is_default = models.BooleanField(default=False)
    hashed_license = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "stores"

    # def delete_cache(self):
    #     from src.client.global_cache import refresh_cache
    #     delete_cache(prefix=STORE_PREFIX, user=self.user, number=self.number)
    #     refresh_cache(self.user)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.handle:
            self.handle = slugify(self.name)
        super().save(*args, **kwargs)
        # self.delete_cache()

    def delete(self, using=None, keep_parents=False):
        # self.delete_cache()
        super().delete(using, keep_parents)

    def has_items(self):
        return self.store_plans.exists()

    def items(self):
        return self.store_plans

    def user_has_items(self):
        return self.store_plans.exists()

    def licence_veryfy(self):
        from src.core.models import License
        licence = License.objects.filter(
            hashed_data=self.hashed_license).first()
        if licence:
            return licence.validate()
        return None

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

    @property
    def user_plans_data(self):
        if not self.user_plans.all().exists():
            return []
        return [{**obj.get_object_tree()} for obj in self.user_plans.all()]
