import django_filters
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework import viewsets
from .serializers import DocumentSerializer
from src.documents.models import Document
from src.core.utils import get_columns, get_indexes
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.accounts.models import Customer

from src.documents.filters import DocumentFilter



# http://127.0.0.1:8000/documents/api/list/?format=datatables&keep=id

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


@api_view(['GET'])
def document_columns_view(request):
    columns = get_columns('documents')  # Assuming you have a get_columns function
    indexes = get_indexes('documents')  # Assuming you have a get_columns function
    return Response({"columns": columns, "indexes": indexes})

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     # Add the columns to the context
    #     context['columns'] = get_columns('documents')  # Assuming you have a get_columns function
    #     return context