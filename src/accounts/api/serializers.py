from rest_framework import serializers
from src.accounts.models import Warehouse

class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'created', 'updated']
