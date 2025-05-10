from django.core.paginator import Paginator
from src.accounts.models import Customer
from src.accounts.filters import CustomersFilter
from src.accounts.models import get_customers

def get_paginated_customer_results(request=None):
    page_number = request.GET.get("page", 1) if request else 1

    customers = get_customers(request.user, refresh=True)
    customer_ids = [customer['id'] for customer in customers]
    customers_queryset = Customer.objects.filter(
        id__in=customer_ids).select_related('user')


    customers_filter = CustomersFilter(request.GET, queryset=customers_queryset)
    filtered_ids = list(customers_filter.qs.values_list("id", flat=True))

    customers = [customer for customer in customers if customer['id'] in filtered_ids]

    paginator = Paginator(customers, 5)
    customer_page_obj = paginator.get_page(page_number)

    return {
        "customers_filter": customers_filter,
        "customers_form": customers_filter.form,
        "customers_page_obj": customer_page_obj,
        "customers": customers,
    }