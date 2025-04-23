from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, BooleanField, ExpressionWrapper, F
from django.contrib.auth.decorators import login_required
from src.stock.models import Stock, StockControl
from src.stock.filters import StockFilter

def search_stock(request):
    stock_controls = StockControl.objects.filter(product=OuterRef('product'))

    queryset = Stock.objects.annotate(
        preferred_quantity=Subquery(stock_controls.values('preferred_quantity')[:1]),
        is_low_stock_warning_enabled=Subquery(stock_controls.values('is_low_stock_warning_enabled')[:1]),
        low_stock_warning_quantity=Subquery(stock_controls.values('low_stock_warning_quantity')[:1]),
    )

    stock_filter = StockFilter(request.GET, queryset=queryset)
    filtered_qs = stock_filter.qs
    form = stock_filter.form

    # Pagination
    # page_number = request.GET.get("page", 1)
    # paginator = Paginator(filtered_qs, 10)
    # page_obj = paginator.get_page(page_number)

    context = {
        "filter": stock_filter,
        "form": form,
        # "page_obj": page_obj,
        "stocks": filtered_qs,
    }

    # if request.htmx:
    #     html = render_to_string("stock/partials/stock_table_rows.html", context, request=request)
    #     return HttpResponse(html)

    return render(request, "cotton/modals/search/products/index.html", context)