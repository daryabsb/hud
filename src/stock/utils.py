from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from src.stock.models import Stock, StockControl, get_stocks
from src.stock.filters import StockFilter
from django.db.models import Prefetch
from collections import OrderedDict

def get_stocks_with_controls(stock_ids):
    stock_control_qs = StockControl.objects.only(
        'product_id', 'preferred_quantity', 'is_low_stock_warning_enabled',
        'low_stock_warning_quantity', 'customer'
    )

    print(stock_control_qs.count())  # Debugging line to check the SQL query

    return Stock.objects.select_related('product').prefetch_related(
        Prefetch(
            'product__stock_controls',
            queryset=stock_control_qs,
            to_attr='prefetched_stockcontrols'
        )
    ).filter(id__in=stock_ids)


def get_paginated_stock_results(request=None):
    page_number = request.GET.get("page", 1) if request else 1

    # 1. Use cached stock list for speed
    stocks = get_stocks(user=request.user)
    stock_filter = StockFilter(request.GET, queryset=None)
    filtered_qs = stocks
    print(f"stock[0]: {stocks[0]}")  # Debugging line to check the filtered IDs
    
    if request.htmx:
        # 2. Refetch filtered queryset from DB using cached IDs
        stock_ids = [stock['id'] for stock in stocks]
        stock_queryset = get_stocks_with_controls(stock_ids)

        # 3. Apply filtering
        stock_filter = StockFilter(request.GET, queryset=stock_queryset)
        filtered_ids = list(stock_filter.qs.values_list("id", flat=True))

        print(f"Filtered IDs: {filtered_ids}")  # Debugging line to check the filtered IDs

        # 4. Reverse-filter the cached list using the filtered IDs
        stockss = [stock for stock in stocks if stock['id'] in filtered_ids]

        print(f"stock[1]: {stockss[0]}")  # Debugging line to check the filtered IDs
        filtered_qs = stock_filter.qs

    paginator = Paginator(filtered_qs, 10)
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
            Prefetch('product__stock_controls', queryset=stock_control_qs, to_attr='prefetched_stockcontrols')
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
                                 ('name', 'Organic Bananas'), ('slug', 'organic bananas'), ('barcode__value', '9583992909021'), 
                                 ('parent_group__name', 'Grocery'), ('price', '1200.000'), ('cost', '0.000'), ('last_purchase_price', '0.000'), 
                                 ('margin', '100.000'), ('measurement_unit', 'KG'), ('currency__name', 'IQD'), ('rank', 1), ('plu', None), 
                                 ('user__name', 'Super Admin'), ('color', '#FFFFFF'), ('description', None), ('is_tax_inclusive_price', False), 
                                 ('is_price_change_allowed', False), ('is_service', False), ('is_using_default_quantity', True), ('is_enabled', True), 
                                 ('age_restriction', None), ('created', '2024-07-13T09:31:16.325602+03:00'), ('updated', '2025-04-22T14:07:13.859242+03:00')
                                 ]
                                )
                            ), 
        ('quantity', 60), 
        ('low_stock_warning_quantity', 12), ('preferred_quantity', 75), ('is_low_stock_warning_enabled', True), ('customer', 4), 
        ('created', '2025-04-22T13:54:20.142611+03:00'), ('updated', '2025-04-23T15:58:41.894346+03:00')])
25

stock_1 = OrderedDict(
    [('id', 1), ('warehouse', OrderedDict([('id', 1), ('name', 'My Warehouse'), ('created', '2024-07-13T09:31:09.037526+03:00'), 
                                        ('updated', '2025-04-22T14:07:10.731908+03:00')])), 
        ('product', OrderedDict([('id', 1), ('code', 'baba1212'), ('image', '/media/uploads/product/7fb638f8-c3a0-4181-b13b-8b7e7bbabe0d.jpg'), 
                                 ('name', 'Organic Bananas'), ('slug', 'organic bananas'), ('barcode__value', '9583992909021'), 
                                 ('parent_group__name', 'Grocery'), ('price', '1200.000'), ('cost', '0.000'), ('last_purchase_price', '0.000'), 
                                 ('margin', '100.000'), ('measurement_unit', 'KG'), ('currency__name', 'IQD'), ('rank', 1), ('plu', None), 
                                 ('user__name', 'Super Admin'), ('color', '#FFFFFF'), ('description', None), ('is_tax_inclusive_price', False), 
                                 ('is_price_change_allowed', False), ('is_service', False), ('is_using_default_quantity', True), ('is_enabled', True), 
                                 ('age_restriction', None), ('created', '2024-07-13T09:31:16.325602+03:00'), ('updated', '2025-04-22T14:07:13.859242+03:00')
                                 ]
                                )), 
        ('quantity', 60), 
        ('low_stock_warning_quantity', 12), ('preferred_quantity', 75), ('is_low_stock_warning_enabled', True), ('customer', 4), 
        ('created', '2025-04-22T13:54:20.142611+03:00'), ('updated', '2025-04-23T15:58:41.894346+03:00')])