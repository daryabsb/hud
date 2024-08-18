from rest_framework import serializers
from src.documents.models import Document
from src.core.utils import get_fields


class DocumentSerializer(serializers.ModelSerializer):
    customer__name = serializers.CharField(source='customer.name', read_only=True)
    user__name = serializers.CharField(source='user.name', read_only=True)
    cash_register__name = serializers.CharField(source='cash_register.name', read_only=True)
    document_type__name = serializers.CharField(source='document_type.name', read_only=True)
    warehouse__name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = Document
        fields = [*get_fields('documents') ]
        # [
        #     'id', 'number', 'customer_name', 'customer', 'user', 'user_name', 'cash_register_name',
        #     'order', 'document_type_name', 'warehouse_name', 'date',
        #     'reference_document_number', 'internal_note', 'note', 'due_date',
        #     'discount', 'discount_type', 'discount_apply_rule', 'paid_status',
        #     'stock_date', 'total', 'is_clocked_out', 'created', 'updated'
        # ]
        datatables_always_serialize = ('id',)
