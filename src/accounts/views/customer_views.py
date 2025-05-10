from django.shortcuts import render
from src.stock.forms import StockControlForm
from src.accounts.forms import CustomerForm
from src.accounts.models import get_customers
from django.contrib.auth.decorators import login_required

@login_required
def customer_profile(request, slug):
    customers = [customer for customer in get_customers(user=request.user)]
    customer = next(
        (customer for customer in customers if customer["slug"] == slug), None)
    return render(request, 'cotton/customers/profile.html', {'customer': customer})

# MANAGEMENT VIEWS
@login_required
def add_new_supplier(request):
    form = CustomerForm(request.POST)

    if form.is_valid():
        customer = form.save(commit=False)
        customer.user = request.user
        customer.is_customer = False
        customer.is_supplier = True
        customer.save()
    stock_control_form = StockControlForm(initial={'customer': customer})
    context = {"stock_control_form": stock_control_form}
    return render(
        request, 'mgt/tabs/add-product/side-forms/customer-field.html', context)


