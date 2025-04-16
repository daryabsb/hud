from django.db import models
from django.db.models import Q, F
from typing import List, Dict, Tuple, Optional
# from src.products.models import Product


class ProductManager(models.Manager):

    def _get_related_fields(self):
        return ['currency', 'barcode', 'parent_group', 'user']

    def filter_by_search_value(self, search_value):
        related_fields = self._get_related_fields()
        qs = super().select_related(*related_fields).annotate(
            user__name=F('user__name'),
            barcode__value=F('barcode__value'),
            parent_group__name=F('parent_group__name'),
            currency__name=F('currency__name'),
        ).order_by("id").filter(
            # qs = qs
            Q(name__icontains=search_value)
            | Q(code__icontains=search_value)
            | Q(barcode__value__icontains=search_value)
            | Q(parent_group__name__icontains=search_value)
            | Q(description__icontains=search_value)
        )
        return qs

    def get_dict_list(self) -> List[Dict]:
        """Returns a list of dictionaries representing Product instances."""
        queryset = self.get_queryset()
        related_fields = self._get_related_fields()
        return [
            {
                'id': product.id,
                'name': product.name,
                'code': product.code,
                'barcode': product.barcode.value if product.barcode else None,
                'parent_group': product.parent_group.name if product.parent_group else None,
                'description': product.description,
                'created': product.created,
                'updated': product.updated,
            }
            for product in queryset.select_related(*related_fields)
        ]

    def filter_by_search(self, search_value: Optional[str] = None) -> Q:
        """Returns a Q object for filtering products based on search value."""
        if not search_value:
            return Q()

        return (
            Q(name__icontains=search_value) |
            Q(code__icontains=search_value) |
            Q(barcode__value__icontains=search_value) |
            Q(parent_group__name__icontains=search_value) |
            Q(description__icontains=search_value)
        )

    def get_related_fields(self) -> List[str]:
        """Returns a list of related fields for select_related."""
        return ['currency', 'barcode', 'parent_group', 'user']
