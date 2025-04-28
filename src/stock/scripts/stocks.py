from src.products.models import Product
from src.stock.models import Stock, StockControl
from django.db.models import Prefetch
from django.forms import model_to_dict
from decimal import Decimal

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
        Prefetch('stock_controls', queryset=stock_control_qs, to_attr='prefetched_stockcontrols')
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
            print(stock_info)

        for stock_control in product.prefetched_stockcontrols:
            stock_control_info = {
                'id': stock_control.id,
                'customer': stock_control.customer.name if stock_control.customer else None,
                'preferred_quantity': stock_control.preferred_quantity,
                'is_low_stock_warning_enabled': stock_control.is_low_stock_warning_enabled,
                'low_stock_warning_quantity': stock_control.low_stock_warning_quantity,
            }
            print(stock_control_info)
        print(product)

    return products

    # stock_control_qs = StockControl.objects.only(
    #     'product_id', 'preferred_quantity', 'is_low_stock_warning_enabled', 'low_stock_warning_quantity'
    # )

    # stock_queryset = Stock.objects.select_related('product').prefetch_related(
    #     Prefetch('product__stock_controls', queryset=stock_control_qs, to_attr='prefetched_stockcontrols')
    # )
    # page_number = request.GET.get("page", 1)



def run():
    get_paginated_stock_results()



'''
    sample_object = products.first()
    print(model_to_dict(sample_object))
sample_object ={
    'id': 1, 'user': 1, 'name': 'Organic Bananas', 'parent_group': 2, 
    'country_of_origin': None, 'code': 'baba1212', 'description': None, 
    'plu': None, 'measurement_unit': 'KG', 'price': Decimal('1200.000'), 
    'currency': 1, 'is_tax_inclusive_price': False, 'is_price_change_allowed': False, 
    'is_service': False, 'is_using_default_quantity': True, 'is_product': True, 
    'cost': Decimal('0.000'), 'margin': Decimal('100.000'), 
    'image': '<ImageFieldFile: uploads/product/7fb638f8-c3a0-4181-b13b-8b7e7bbabe0d.jpg>', 
    'color': '#FFFFFF', 'is_enabled': True, 'age_restriction': None, 
    'last_purchase_price': Decimal('0.000'), 'rank': 1}
'''