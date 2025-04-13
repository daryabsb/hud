from django.db import models
from django.db.models import Q, F
from typing import List, Dict, Tuple, Optional
# from src.products.models import Product


class ProductManager(models.Manager):

    def get_fields(self) -> List[str]:
        """Returns a list of field names for the given app_name."""
        from src.configurations.models import AppTableColumn
        columns = AppTableColumn.objects.filter(app='products')
        return [
            column.related_value if column.is_related else column.name
            for column in columns
        ]

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

    def get_columns(self) -> List[Dict]:
        """Returns a list of column configurations for the given app_name."""
        from src.configurations.models import AppTableColumn
        columns = AppTableColumn.objects.filter(app='products')
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

    def get_indexes(self) -> Dict[str, int]:
        """Returns a dictionary mapping column names to their indexes."""
        print('indees called')
        from src.configurations.models import AppTableColumn
        columns = AppTableColumn.objects.filter(app='products')
        indexes = {column.name: index for index, column in enumerate(columns)}
        indexes['start_date'] = len(indexes)
        indexes['end_date'] = len(indexes)
        return indexes

    def get_searchable_fields(self, app_name: str, fields: Optional[List[str]] = None) -> Tuple[List[str], List[Dict], Dict[str, int]]:
        """Returns searchable fields, columns, and their indexes."""
        fields_list = self.get_fields()
        columns = self.get_columns()
        indexes = self.get_indexes()
        return fields_list, columns, indexes

    def get_dict_list(self) -> List[Dict]:
        """Returns a list of dictionaries representing Product instances."""
        queryset = self.get_queryset()
        return [
            {
                'id': product.id,
                'name': product.name,
                'code': product.code,
                'barcode': product.barcode.value if product.barcode else None,
                'parent_group': product.parent_group.name if product.parent_group else None,
                'description': product.description,
                'start_date': product.start_date,
                'end_date': product.end_date,
            }
            for product in queryset.select_related('parent_group', 'barcode')
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
