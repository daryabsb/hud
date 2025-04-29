from rest_framework import serializers
from src.orders.models import PosOrder, PosOrderItem
from src.products.api.serializers import ProductSerializer
from decimal import Decimal
from collections import OrderedDict
# from src.core.utils import get_fields

# orders/api/serializers.py


class PosOrderItemSerializer(serializers.ModelSerializer):
    # warehouse_id = serializers.IntegerField(source='warehouse.id', read_only=True)
    # warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = PosOrderItem
        # fields = [*get_fields('items'),]
        fields = [
            'number','order','product','round_number','quantity','price','is_locked','discount','discount_type',
            'discounted_amount','discount_sign','item_total','is_featured','voided_by','comment',
            'bundle','created','updated',
        ]

class PosOrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    items = PosOrderItemSerializer(many=True)

    class Meta:
        model = PosOrder
        # fields = [*get_fields('orders'),]
        fields = [
            'number','customer','items','item_subtotal','document_type','warehouse','date',
            'reference_document_number','internal_note','note','due_date','discount',
            'discount_type','discounted_amount','discount_sign','subtotal_after_discount',
            'fixed_taxes','total_tax_rate','total_tax','total','paid_status','is_active',
            'customer_id','customer_name','is_enabled','created','updated'
            ]


orderedDict = (
    [
        ('number', 'sales-06122024-3773'), 
        ('customer', 2), 
        ('items', [
            OrderedDict(
                [('number', 'item-1-06122024-01-3395'), ('order', 'sales-06122024-3773'), ('product', 1), 
                 ('round_number', '0.000'), ('quantity', 4), ('price', '1200.000'), ('is_locked', False), 
                 ('discount', 0.0), ('discount_type', 0.0), ('discounted_amount', Decimal('0.000')), 
                 ('discount_sign', '$'), ('item_total', Decimal('4800.000')), ('is_featured', False), 
                 ('voided_by', 0), ('comment', None), ('bundle', None), 
                 ('created', '2024-12-06T16:02:02.046929+03:00'), 
                 ('updated', '2025-04-05T15:21:36.321780+03:00')]
                 ), 
            OrderedDict(
                [('number', 'item-1-07122024-01-0471'), ('order', 'sales-06122024-3773'), ('product', 4), 
                 ('round_number', '0.000'), ('quantity', 4), ('price', '8000.000'), ('is_locked', False), 
                 ('discount', 0.0), ('discount_type', 0.0), ('discounted_amount', Decimal('0.000')), 
                 ('discount_sign', '$'), ('item_total', Decimal('32000.000')), ('is_featured', False), 
                 ('voided_by', 0), ('comment', None), ('bundle', None), 
                 ('created', '2024-12-07T12:30:16.901404+03:00'), 
                 ('updated', '2025-04-05T15:29:40.589335+03:00')]
                 )
                ]
            ), 
            ('item_subtotal', '36800.000'), 
            ('document_type', 2), ('warehouse', 1), 
            ('date', '2024-12-06T16:00:19.008749+03:00'), 
            ('reference_document_number', None), 
            ('internal_note', ''), 
            ('note', 'This is an active comment from the admin, revised'), 
            ('due_date', '2024-12-06T16:00:19.008749+03:00'), ('discount', 0.0), ('discount_type', 0.0), 
            ('discounted_amount', Decimal('0.000')), ('discount_sign', '$'), 
            ('subtotal_after_discount', Decimal('36800.000')), ('fixed_taxes', '0.000'), 
            ('total_tax_rate', '5.000'), ('total_tax', Decimal('1840.000')), ('total', Decimal('38640.000')), 
            ('paid_status', False), ('is_active', True), ('customer_id', 2), ('customer_name', 'Maad Center'), 
            ('is_enabled', True), ('created', '2024-12-06T16:00:19.008749+03:00'), 
            ('updated', '2025-04-23T16:10:18.991071+03:00')
            ]
        )

order = OrderedDict(
    [
        ('number', 'sales-06122024-3773'), ('customer', 2), 
        ('items', [
            OrderedDict(
                [('number', 'item-1-06122024-01-3395'), ('order', 'sales-06122024-3773'), 
                ('product', OrderedDict(
                    [('id', 1), ('code', 'baba1212'), ('image', '/media/uploads/product/7fb638f8-c3a0-4181-b13b-8b7e7bbabe0d.jpg'), 
                    ('name', 'Organic Bananas'), ('slug', 'organic bananas'), ('barcode__value', '9583992909021'), 
                    ('parent_group__name', 'Grocery'), ('price', '1200.000'), ('cost', '0.000'), ('last_purchase_price', '0.000'), 
                    ('margin', '100.000'), ('measurement_unit', 'KG'), ('currency__name', 'IQD'), ('rank', 1), ('plu', None), 
                    ('user__name', 'Super Admin'), ('color', '#FFFFFF'), ('description', None), ('is_tax_inclusive_price', False), 
                    ('is_price_change_allowed', False), ('is_service', False), ('is_using_default_quantity', True), ('is_enabled', True), 
                    ('age_restriction', None), ('created', '2024-07-13T09:31:16.325602+03:00'), ('updated', '2025-04-22T14:07:13.859242+03:00')
                    ]
                    )
                    ), 
                ('round_number', '0.000'), ('quantity', 4), ('price', '1200.000'), ('is_locked', False), ('discount', 0.0), 
                ('discount_type', 0.0), ('discounted_amount', Decimal('0.000')), ('discount_sign', '$'), ('item_total', Decimal('4800.000')), 
                ('is_featured', False), ('voided_by', 0), ('comment', None), ('bundle', None), ('created', '2024-12-06T16:02:02.046929+03:00'), 
                ('updated', '2025-04-05T15:21:36.321780+03:00')]
                ), 
            OrderedDict(
                [('number', 'item-1-07122024-01-0471'), ('order', 'sales-06122024-3773'), 
                ('product', OrderedDict(
                    [('id', 4), ('code', None), ('image', '/media/initial/sourdoughbread.jpg'), 
                     ('name', 'Sourdough Bread'), ('slug', 'sourdoughbread'), ('barcode__value', '9502512919173'), 
                     ('parent_group__name', 'Grocery'), ('price', '4000.000'), ('cost', '0.000'), ('last_purchase_price', '0.000'), 
                     ('margin', '100.000'), ('measurement_unit', 'pcs'), ('currency__name', 'IQD'), ('rank', 4), ('plu', None), 
                     ('user__name', 'Super Admin'), ('color', '#FFFFFF'), ('description', None), ('is_tax_inclusive_price', False), 
                     ('is_price_change_allowed', False), ('is_service', False), ('is_using_default_quantity', True), ('is_enabled', True), 
                     ('age_restriction', None), ('created', '2024-07-13T09:31:18.432514+03:00'), ('updated', '2025-04-22T14:07:14.224753+03:00')
                     ]
                     )
                     ), 
                ('round_number', '0.000'), ('quantity', 4), ('price', '8000.000'), ('is_locked', False), ('discount', 0.0), 
                ('discount_type', 0.0), ('discounted_amount', Decimal('0.000')), ('discount_sign', '$'), ('item_total', Decimal('32000.000')), 
                ('is_featured', False), ('voided_by', 0), ('comment', None), ('bundle', None), ('created', '2024-12-07T12:30:16.901404+03:00'), 
                ('updated', '2025-04-05T15:29:40.589335+03:00')
                ]
            )
            ]), ('item_subtotal', '36800.000'), ('document_type', 2), ('warehouse', 1), 
                ('date', '2024-12-06T16:00:19.008749+03:00'), ('reference_document_number', None), ('internal_note', ''), 
                ('note', 'This is an active comment from the admin, revised'), ('due_date', '2024-12-06T16:00:19.008749+03:00'), ('discount', 0.0), 
                ('discount_type', 0.0), ('discounted_amount', Decimal('0.000')), ('discount_sign', '$'), ('subtotal_after_discount', Decimal('36800.000')), 
                ('fixed_taxes', '0.000'), ('total_tax_rate', '5.000'), ('total_tax', Decimal('1840.000')), ('total', Decimal('38640.000')), 
                ('paid_status', False), ('is_active', True), ('customer_id', 2), ('customer_name', 'Maad Center'), ('is_enabled', True), ('created', '2024-12-06T16:00:19.008749+03:00'), ('updated', '2025-04-23T16:10:18.991071+03:00')])