from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from src.stock.models import Stock, StockControl, get_stocks
from src.stock.filters import StockFilter
from django.db.models import Prefetch
from collections import OrderedDict
from src.pos2.forms import PosOrderItemForm
from src.products.models import Product


def get_merged_stock_data(user=None, warehouse=None, customer=None):
    # Step 1: Filter stocks
    stocks = Stock.objects.select_related('product').all()

    if user and not (user.is_staff or user.is_superuser):
        stocks = stocks.filter(user=user)

    if warehouse:
        stocks = stocks.filter(warehouse=warehouse)

    # Step 2: Fetch all stock controls in one query
    product_ids = [stock.product_id for stock in stocks]
    stock_controls = StockControl.objects.filter(
        product_id__in=product_ids
        ).select_related('customer').only('product_id', 'preferred_quantity', 'is_low_stock_warning_enabled',
            'low_stock_warning_quantity', 'customer__name')

    # Step 3: Map product_id -> stock_control
    control_map = {sc.product_id: sc for sc in stock_controls}

    # Step 4: Merge data
    merged_stocks = []
    for stock in stocks:
        control = control_map.get(stock.product_id)
        stock_dict = {
            "id": stock.id,
            "product_id": stock.product.id,
            "product_name": stock.product.name,
            "product_image": stock.product.image.url,
            "product_group": stock.product.parent_group.name,
            "quantity": stock.quantity,
            "warehouse": stock.warehouse.name,
            # Add control info if available
            "customer": getattr(control.customer, "name", None),
            "preferred_quantity": getattr(control, "preferred_quantity", None),
            "low_stock_warning_quantity": getattr(control, "low_stock_warning_quantity", None),
            "is_low_stock_warning_enabled": getattr(control, "is_low_stock_warning_enabled", False),
            # Add more stock or control fields as needed
        }
        merged_stocks.append(stock_dict)

    return merged_stocks

def get_stocks_with_controls(stock_ids):

    return Stock.objects.select_related('product').filter(id__in=stock_ids)


def get_paginated_stock_results(request=None):
    page_number = request.GET.get("page", 1) if request else 1

    # 1. Use cached stock list for speed
    stocks = [stock for stock in get_stocks(user=request.user)]

    stock_ids = [stock['id'] for stock in stocks]
    stock_queryset = get_stocks_with_controls(stock_ids)

    # 3. Apply filtering
    stock_filter = StockFilter(request.GET, queryset=stock_queryset)
    filtered_ids = list(stock_filter.qs.values_list("id", flat=True))

    # 4. Reverse-filter the cached list using the filtered IDs
    stocks = [stock for stock in stocks if stock['id'] in filtered_ids]

    # 5. Create a PosOrderItemForm for each stock item
    for stock in stocks:
        # Initialize form with product_id and default quantity=1
        stock['order_item_form'] = PosOrderItemForm(initial={
            'product': stock['product_id'],
            'quantity': 1
        })

    filtered_qs = stock_filter.qs

    paginator = Paginator(stocks, 5)
    stock_page_obj = paginator.get_page(page_number)

    return {
        "filter": stock_filter,
        "form": stock_filter.form,
        "page_obj": stock_page_obj,
        "stocks": stocks,
    }


def get_paginated_stock_results2(request=None):
    # Prefetch related StockControl records for each Stock's product
    if request is not None:
        stock_control_qs = StockControl.objects.only(
            'product_id', 'preferred_quantity', 'is_low_stock_warning_enabled', 'low_stock_warning_quantity'
        )

        stock_queryset = Stock.objects.select_related('product').prefetch_related(
            Prefetch('product__stock_controls', queryset=stock_control_qs,
                     to_attr='prefetched_stockcontrols')
        )
        page_number = request.GET.get("page", 1)

    # stock_filter = StockFilter(request.GET, queryset=stock_queryset)
    stock_filter = StockFilter(queryset=stock_queryset)
    filtered_qs = stock_filter.qs
    form = stock_filter.form

    paginator = Paginator(filtered_qs, 10)
    stock_page_obj = paginator.get_page(page_number)

    return {
        "filter": stock_filter,
        "form": form,
        "page_obj": stock_page_obj,
        "stocks": stock_page_obj.object_list,  # ⚡ Only paginated, not full filtered_qs
    }


stock = OrderedDict(
    [('id', 1), ('warehouse', OrderedDict([('id', 1), ('name', 'My Warehouse'), ('created', '2024-07-13T09:31:09.037526+03:00'),
                                           ('updated', '2025-04-22T14:07:10.731908+03:00')])),
        ('product', OrderedDict([('id', 1), ('code', 'baba1212'), ('image', '/media/uploads/product/7fb638f8-c3a0-4181-b13b-8b7e7bbabe0d.jpg'),
                                 ('name', 'Organic Bananas'), ('slug',
                                                               'organic bananas'), ('barcode__value', '9583992909021'),
                                 ('parent_group__name', 'Grocery'), ('price', '1200.000'), (
                                     'cost', '0.000'), ('last_purchase_price', '0.000'),
                                 ('margin', '100.000'), ('measurement_unit',
                                                         'KG'), ('currency__name', 'IQD'), ('rank', 1), ('plu', None),
                                 ('user__name', 'Super Admin'), ('color', '#FFFFFF'), (
                                     'description', None), ('is_tax_inclusive_price', False),
                                 ('is_price_change_allowed', False), ('is_service', False), (
                                     'is_using_default_quantity', True), ('is_enabled', True),
                                 ('age_restriction', None), ('created',
                                                             '2024-07-13T09:31:16.325602+03:00'), ('updated', '2025-04-22T14:07:13.859242+03:00')
                                 ]
                                )
         ),
        ('quantity', 60),
        ('low_stock_warning_quantity', 12), ('preferred_quantity',
                                             75), ('is_low_stock_warning_enabled', True), ('customer', 4),
        ('created', '2025-04-22T13:54:20.142611+03:00'), ('updated', '2025-04-23T15:58:41.894346+03:00')])
25

stock_1 = OrderedDict(
    [('id', 1), ('warehouse', OrderedDict([('id', 1), ('name', 'My Warehouse'), ('created', '2024-07-13T09:31:09.037526+03:00'),
                                           ('updated', '2025-04-22T14:07:10.731908+03:00')])),
        ('product', OrderedDict([('id', 1), ('code', 'baba1212'), ('image', '/media/uploads/product/7fb638f8-c3a0-4181-b13b-8b7e7bbabe0d.jpg'),
                                 ('name', 'Organic Bananas'), ('slug',
                                                               'organic bananas'), ('barcode__value', '9583992909021'),
                                 ('parent_group__name', 'Grocery'), ('price', '1200.000'), (
                                     'cost', '0.000'), ('last_purchase_price', '0.000'),
                                 ('margin', '100.000'), ('measurement_unit',
                                                         'KG'), ('currency__name', 'IQD'), ('rank', 1), ('plu', None),
                                 ('user__name', 'Super Admin'), ('color', '#FFFFFF'), (
                                     'description', None), ('is_tax_inclusive_price', False),
                                 ('is_price_change_allowed', False), ('is_service', False), (
                                     'is_using_default_quantity', True), ('is_enabled', True),
                                 ('age_restriction', None), ('created',
                                                             '2024-07-13T09:31:16.325602+03:00'), ('updated', '2025-04-22T14:07:13.859242+03:00')
                                 ]
                                )),
        ('quantity', 60),
        ('low_stock_warning_quantity', 12), ('preferred_quantity',
                                             75), ('is_low_stock_warning_enabled', True), ('customer', 4),
        ('created', '2025-04-22T13:54:20.142611+03:00'), ('updated', '2025-04-23T15:58:41.894346+03:00')])


[
    
    {'id': 1, 'product_id': 1, 'product_name': 'Organic Bananas', 'product_group': 'Grocery', 
        'quantity': 60, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 75, 
        'low_stock_warning_quantity': 12, 'is_low_stock_warning_enabled': True}, 
    {'id': 2, 'product_id': 2, 'product_name': 'Whole Milk', 'product_group': 'Grocery', 
        'quantity': 25, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 50, 
        'low_stock_warning_quantity': 12, 'is_low_stock_warning_enabled': True}, 
    {'id': 3, 'product_id': 3, 'product_name': 'Chicken Breast', 'product_group': 'Grocery', 
        'quantity': 30, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 50, 
        'low_stock_warning_quantity': 9, 'is_low_stock_warning_enabled': True}, 
    {'id': 4, 'product_id': 4, 'product_name': 'Sourdough Bread', 'product_group': 'Grocery', 
        'quantity': 30, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 50, 
        'low_stock_warning_quantity': 9, 'is_low_stock_warning_enabled': True}, 
    {'id': 5, 'product_id': 5, 'product_name': 'Tomato Soup', 'product_group': 'Grocery', 
        'quantity': 55, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 50, 
        'low_stock_warning_quantity': 18, 'is_low_stock_warning_enabled': True}, 
    {'id': 6, 'product_id': 6, 'product_name': 'Phone Pro Max', 'product_group': 'Electronics', 
        'quantity': 15, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 15, 
        'low_stock_warning_quantity': 9, 'is_low_stock_warning_enabled': True}, 
    {'id': 7, 'product_id': 7, 'product_name': 'DELL Lavender', 'product_group': 'Electronics', 
        'quantity': 18, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 15, 
        'low_stock_warning_quantity': 6, 'is_low_stock_warning_enabled': True}, 
    {'id': 22, 'product_id': 22, 'product_name': 'Potato Chips', 'product_group': 'Goodies', 
        'quantity': 45, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 35, 
        'low_stock_warning_quantity': 18, 'is_low_stock_warning_enabled': True}, 
    {'id': 23, 'product_id': 23, 'product_name': 'Gummy Bears', 'product_group': 'Goodies', 
        'quantity': 50, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 35, 
        'low_stock_warning_quantity': 18, 'is_low_stock_warning_enabled': True}, 
    {'id': 24, 'product_id': 24, 'product_name': 'Truffle Oil', 'product_group': 'Goodies', 
        'quantity': 15, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 15, 
        'low_stock_warning_quantity': 6, 'is_low_stock_warning_enabled': True}, 
    {'id': 25, 'product_id': 25, 'product_name': 'Holiday Gift Basket', 'product_group': 'Goodies', 
        'quantity': 11, 'warehouse': 'My Warehouse', 'customer': None, 'preferred_quantity': 15, 
        'low_stock_warning_quantity': 6, 'is_low_stock_warning_enabled': True}
]
