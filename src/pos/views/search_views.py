from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.stock.utils import get_paginated_stock_results
from src.accounts.utils import get_paginated_customer_results


@login_required
def search_stock(request):
    stock_context = get_paginated_stock_results(request)
    is_next = request.GET.get("is_next") == "1"
    if is_next:
        return render(request, 'cotton/modals/search/products/rows.html', stock_context)
    return render(request, "cotton/modals/search/products/index.html", stock_context)


@login_required
def search_customers(request):
    customers_context = get_paginated_customer_results(request)
    is_next = request.GET.get("is_next") == "1"
    if is_next:
        return render(request, 'cotton/modals/search/customers/rows.html', customers_context)
    return render(request, "cotton/modals/search/customers/index.html", customers_context)
