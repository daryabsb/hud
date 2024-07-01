from django.shortcuts import render
from src.stock.forms import StockControlForm
from src.accounts.forms import CustomerForm


# MANAGEMENT VIEWS
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

