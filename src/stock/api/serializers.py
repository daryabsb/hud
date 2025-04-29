from rest_framework import serializers
from src.stock.models import StockControl, Stock
from src.products.api.serializers import ProductSerializer
from src.accounts.api.serializers import WarehouseSerializer
from decimal import Decimal
from collections import OrderedDict
# from src.core.utils import get_fields

# orders/api/serializers.py


class StockControlSerializer(serializers.ModelSerializer):
    # warehouse_id = serializers.IntegerField(source='warehouse.id', read_only=True)

    class Meta:
        model = StockControl
        # fields = [*get_fields('items'),]
        fields = [
            'id','low_stock_warning_quantity','preferred_quantity',
            'is_low_stock_warning_enabled','customer','created','updated',
        ]


class StockSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    low_stock_warning_quantity = serializers.SerializerMethodField()
    preferred_quantity = serializers.SerializerMethodField()
    is_low_stock_warning_enabled = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        # fields = [*get_fields('orders'),]
        fields = [
            'id','warehouse','product','quantity','low_stock_warning_quantity','preferred_quantity',
            'is_low_stock_warning_enabled','customer','created','updated'
            ]
    def get_stock_control(self, obj):
        # You can add filtering logic here, e.g., by warehouse/customer if needed
        return obj.product.stock_controls.first()

    def get_low_stock_warning_quantity(self, obj):
        # Assumes product.prefetched_stockcontrols is a list (due to `to_attr='prefetched_stockcontrols'`)
        control = self.get_stock_control(obj)
        return control.low_stock_warning_quantity if control else None

    def get_preferred_quantity(self, obj):
        control = self.get_stock_control(obj)
        return control.preferred_quantity if control else None

    def get_is_low_stock_warning_enabled(self, obj):
        control = self.get_stock_control(obj)
        return control.is_low_stock_warning_enabled if control else None

    def get_customer(self, obj):
        control = self.get_stock_control(obj)
        return control.customer_id if control else None  # or use CustomerSerializer(control.customer).data
