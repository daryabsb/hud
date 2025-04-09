from rest_framework import serializers
from src.products.models import Product
from src.core.utils import get_fields


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name',]
        datatables_always_serialize = ('id',)