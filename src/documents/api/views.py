


import django_filters
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework import viewsets
from .serializers import DocumentSerializer
from src.documents.models import Document

class DocumentFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    user = django_filters.CharFilter(field_name='user__name', lookup_expr='icontains')
    document_type = django_filters.CharFilter(field_name='document_type__name', lookup_expr='icontains')
    cash_register = django_filters.CharFilter(field_name='cash_register__name', lookup_expr='icontains')
    warehouse = django_filters.CharFilter(field_name='warehouse__name', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name='created', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Document
        fields = ['customer', 'user', 'document_type', 'cash_register', 'warehouse', 'start_date', 'end_date']



class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related(
        'user', 'customer', 'cash_register', 'order', 'document_type', 'warehouse'
    ).all()
    serializer_class = DocumentSerializer
    filter_backends = (DatatablesFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    filterset_class = DocumentFilter

    def get_queryset(self):
        # Customize queryset if needed based on request
        return self.queryset