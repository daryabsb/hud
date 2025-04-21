from rest_framework import serializers
from src.finances.models import PaymentType
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentTypeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = PaymentType
        fields = [
            'id',
            'user',
            'name',
            'code',
            'is_customer_required',
            'is_fiscal',
            'is_slip_required',
            'is_change_allowed',
            'ordinal',
            'is_enabled',
            'is_quick_payment',
            'open_cash_drawer',
            'shortcut',
            'mark_as_paid',
            'created',
            'updated',
        ]
        read_only_fields = ['created', 'updated']