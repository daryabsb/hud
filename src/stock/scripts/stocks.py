from src.products.models import Product
from src.stock.models import Stock, StockControl
from src.stock.api.serializers import StockSerializer
from django.db.models import Prefetch
from django.forms import model_to_dict
from decimal import Decimal
from collections import OrderedDict


def get_paginated_stock_results(request=None):

    stock_control_qs = StockControl.objects.select_related('customer').only(
        'customer',
        'preferred_quantity',
        'is_low_stock_warning_enabled',
        'low_stock_warning_quantity',
    )
    stocks_qs = Stock.objects.select_related('warehouse').only(
        'quantity',
        'warehouse',
    )

    products = Product.objects.prefetch_related(
        Prefetch('stocks', queryset=stocks_qs, to_attr='prefetched_stocks'),
        Prefetch('stock_controls', queryset=stock_control_qs,
                 to_attr='prefetched_stockcontrols')
    ).select_related(
        'parent_group'
    ).only(
        'id',
        'name',
        'image',
        'parent_group',
    )
    for product in products:
        for stock in product.prefetched_stocks:
            stock_info = {
                'id': stock.id,
                'product_name': product.name,
                'group_name': product.parent_group.name if product.parent_group else None,
                'stock_quantity': stock.quantity,
                'warehouse_name': stock.warehouse.name if stock.warehouse else None,
            }
            # print(stock_info)

        for stock_control in product.prefetched_stockcontrols:
            stock_control_info = {
                'id': stock_control.id,
                'customer': stock_control.customer.name if stock_control.customer else None,
                'preferred_quantity': stock_control.preferred_quantity,
                'is_low_stock_warning_enabled': stock_control.is_low_stock_warning_enabled,
                'low_stock_warning_quantity': stock_control.low_stock_warning_quantity,
            }
            # print(stock_control_info)
        print(
            f'[id: {product.id},name: {product.name},image: {product.image.url},parent_group: {product.parent_group}]')

    return products

    # stock_control_qs = StockControl.objects.only(
    #     'product_id', 'preferred_quantity', 'is_low_stock_warning_enabled', 'low_stock_warning_quantity'
    # )

    # stock_queryset = Stock.objects.select_related('product').prefetch_related(
    #     Prefetch('product__stock_controls', queryset=stock_control_qs, to_attr='prefetched_stockcontrols')
    # )
    # page_number = request.GET.get("page", 1)

def test_stocks_serializer():
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    print(serializer.data[0])

def run():
    # get_paginated_stock_results()
    test_stocks_serializer()


stock_0 = OrderedDict(
    [
        ('id', 1), ('warehouse', OrderedDict([('id', 1), ('name', 'My Warehouse'), ('created', '2024-07-13T09:31:09.037526+03:00'), 
        ('updated', '2025-04-22T14:07:10.731908+03:00')])), 
        ('product', OrderedDict(
            [('id', 1), ('code', 'baba1212'), ('image', '/media/uploads/product/7fb638f8-c3a0-4181-b13b-8b7e7bbabe0d.jpg'), 
            ('name', 'Organic Bananas'), ('slug', 'organic bananas'), ('barcode__value', '9583992909021'), ('parent_group__name', 'Grocery'), 
            ('price', '1200.000'), ('cost', '0.000'), ('last_purchase_price', '0.000'), ('margin', '100.000'), ('measurement_unit', 'KG'), 
            ('currency__name', 'IQD'), ('rank', 1), ('plu', None), ('user__name', 'Super Admin'), ('color', '#FFFFFF'), ('description', None), 
            ('is_tax_inclusive_price', False), ('is_price_change_allowed', False), ('is_service', False), ('is_using_default_quantity', True), 
            ('is_enabled', True), ('age_restriction', None), ('created', '2024-07-13T09:31:16.325602+03:00'), 
            ('updated', '2025-04-22T14:07:13.859242+03:00')])), ('quantity', 60), ('low_stock_warning_quantity', 12), ('preferred_quantity', 75), 
            ('is_low_stock_warning_enabled', True), ('customer', 4), ('created', '2025-04-22T13:54:20.142611+03:00'), 
            ('updated', '2025-04-23T15:58:41.894346+03:00')
        ]
    )