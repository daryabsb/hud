from django.db import models
from django.db.models import Q, F
from typing import List, Dict, Tuple, Optional
# from src.products.models import Product


class DocumentManager(models.Manager):

    def _get_related_fields(self):
        return ['customer', 'cash_register', 'document_type', 'warehouse', 'user']

    def filter_by_search_value(self, search_value):
        related_fields = self._get_related_fields()
        qs = super().select_related(*related_fields).annotate(
            customer__name=F('customer__name'),
            cash_register__name=F('cash_register__name'),
            document_type__code=F('document_type__code'),
            warehouse__name=F('warehouse__name'),
            user__name=F('user__name'),
        ).order_by("id").filter(
            # qs = qs
            Q(number__icontains=search_value)
            | Q(document_type__code__icontains=search_value)
            | Q(customer__name__icontains=search_value)
            | Q(warehouse__name__icontains=search_value)
            | Q(cash_register__name__icontains=search_value)
            | Q(reference_document_number__icontains=search_value)
        )
        return qs

    def get_dict_list(self) -> List[Dict]:
        """Returns a list of dictionaries representing Product instances."""
        queryset = self.get_queryset()
        related_fields = self._get_related_fields()
        return [
            {
                'number': document.number,
                'customer': document.customer.name if document.customer else None,
                'cash_register': document.cash_register.name if document.cash_register else None,
                'user': document.user.name if document.user else None,
                'note': document.note,
                'created': document.created,
                'updated': document.updated,
            }
            for document in queryset.select_related(*related_fields)
        ]
