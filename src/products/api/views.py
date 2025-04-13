from rest_framework import viewsets
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from src.products.api.serializers import ProductSerializer
from src.products.models import Product
from src.core.utils import get_columns, get_indexes
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.select_related(
    #     'user', 'customer', 'cash_register', 'order', 'document_type', 'warehouse'
    # ).all()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DatatablesFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    # filterset_class = DocumentFilter
    filterset_fields = '__all__'

    def get_queryset(self):
        # Customize queryset if needed based on request
        return self.queryset


@api_view(['GET'])
def products_columns_view(request):
    # Assuming you have a get_columns function
    columns = get_columns('products')
    # Assuming you have a get_columns function
    indexes = get_indexes('products')
    return Response({"columns": columns, "indexes": indexes})
