from src.products.models import Product
from src.stock.models import Stock, StockControl
from src.stock.api.serializers import StockSerializer
from django.db.models import Prefetch
from django.forms import model_to_dict
from decimal import Decimal
from collections import OrderedDict
from src.stock.models import get_stocks


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
    # test_stocks_serializer()
    print(get_stocks(refresh=True)[0])

