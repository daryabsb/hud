from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from src.stock.utils import get_paginated_stock_results
from src.accounts.utils import get_paginated_customer_results
from src.pos2.utils import get_active_order
from src.pos2.utils import prepare_order_context


@login_required
@require_GET
def pos_search_modal(request):
    from src.stock.utils import get_paginated_stock_results
    from src.accounts.utils import get_paginated_customer_results
    from src.orders.models import get_orders

    orders = get_orders(user=request.user)
    active_order = get_active_order(user=request.user)

    if active_order is None:
        print("No active order found")

    stock_context = get_paginated_stock_results(request)
    customers_context = get_paginated_customer_results(request)

    context = prepare_order_context(request)
    context.update(stock_context)
    context.update(customers_context)
    is_next = request.GET.get("is_next") == "1"
    if is_next:
        return render(request, 'cotton/pos/modals/search/products/rows.html', context)
    return render(request, 'cotton/pos/modals/search/index.html', context)


@login_required
def search_stock(request):
    stock_context = get_paginated_stock_results(request)
    customers_context = get_paginated_customer_results(request)

    context = prepare_order_context(request)
    context.update(stock_context)
    context.update(customers_context)
    is_next = request.GET.get("is_next") == "1"
    if is_next:
        return render(request, 'cotton/pos/modals/search/products/rows.html', context)
    return render(request, "cotton/pos/modals/search/products/index.html", context)

@login_required
def search_customers(request):
    customers_context = get_paginated_customer_results(request)
    is_next = request.GET.get("is_next") == "1"
    if is_next:
        return render(request, 'cotton/pos/modals/search/customers/rows.html', customers_context)
    return render(request, "cotton/pos/modals/search/customers/index.html", customers_context)
