from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from src.stock.models import Stock, StockControl
from src.stock.filters import StockFilter


def get_paginated_stock_results(request):
    stock_controls = StockControl.objects.filter(product=OuterRef('product'))
    stock_queryset = Stock.objects.annotate(
        preferred_quantity=Subquery(
            stock_controls.values('preferred_quantity')[:1]),
        is_low_stock_warning_enabled=Subquery(
            stock_controls.values('is_low_stock_warning_enabled')[:1]),
        low_stock_warning_quantity=Subquery(
            stock_controls.values('low_stock_warning_quantity')[:1]),
    )

    stock_filter = StockFilter(request.GET, queryset=stock_queryset)
    filtered_qs = stock_filter.qs
    form = stock_filter.form

    page_number = request.GET.get("page", 1)
    paginator = Paginator(filtered_qs, 10)
    stock_page_obj = paginator.get_page(page_number)
    return {
        "filter": stock_filter,
        "form": form,
        "page_obj": stock_page_obj,
        "stocks": filtered_qs,
    }
