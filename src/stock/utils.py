from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from src.stock.models import Stock, StockControl
from src.stock.filters import StockFilter
from django.db.models import Prefetch

def get_paginated_stock_results(request=None):
    # Prefetch related StockControl records for each Stock's product
    if request is not None:
        stock_control_qs = StockControl.objects.only(
            'product_id', 'preferred_quantity', 'is_low_stock_warning_enabled', 'low_stock_warning_quantity'
        )

        stock_queryset = Stock.objects.select_related('product').prefetch_related(
            Prefetch('product__stock_controls', queryset=stock_control_qs, to_attr='prefetched_stockcontrols')
        )
        page_number = request.GET.get("page", 1)
    else:
        stock_queryset = None
        page_number = 1


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

