from rest_framework import serializers
from src.documents.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    cash_register_name = serializers.CharField(source='cash_register.name', read_only=True)
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'number', 'customer_name', 'customer', 'user', 'user_name', 'cash_register_name',
            'order', 'document_type_name', 'warehouse_name', 'date',
            'reference_document_number', 'internal_note', 'note', 'due_date',
            'discount', 'discount_type', 'discount_apply_rule', 'paid_status',
            'stock_date', 'total', 'is_clocked_out', 'created', 'updated'
        ]
        datatables_always_serialize = ('id',)