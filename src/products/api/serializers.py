

from rest_framework import serializers
from src.products.models import Product
from src.core.utils import get_fields, get_columns


class DatatableProductSerializer(serializers.ModelSerializer):

    barcode__value = serializers.CharField(
        source='barcode.value', read_only=True)
    user__name = serializers.CharField(source='user.name', read_only=True)
    parent_group__name = serializers.CharField(
        source='parent_group.name', read_only=True)
    currency__name = serializers.CharField(
        source='currency.name', read_only=True)
    # warehouse__name = serializers.CharField(
    #     source='warehouse.name', read_only=True)

    class Meta:
        model = Product
        fields = [*get_fields('products'),]
        datatables_always_serialize = ('id',)

class ProductSerializer(serializers.ModelSerializer):

    barcode__value = serializers.CharField(
        source='barcode.value', read_only=True)
    user__name = serializers.CharField(source='user.name', read_only=True)
    parent_group__name = serializers.CharField(
        source='parent_group.name', read_only=True)
    currency__name = serializers.CharField(
        source='currency.name', read_only=True)
    
    # warehouse__name = serializers.CharField(
    #     source='warehouse.name', read_only=True)

    class Meta:
        model = Product
        fields = [*get_fields('products'),]
        datatables_always_serialize = ('id',)

