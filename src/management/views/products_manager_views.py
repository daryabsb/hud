from django.shortcuts import render
from src.products.models import Product
from src.products.forms import ProductForm
from src.stock.models import Stock
# Create your views here.


def mgt_products(request):
    products = Product.objects.all()
    return render(request, 'mgt/products/list.html', {"products": products})


def mgt_stocks(request):
    stocks = Stock.objects.all()
    form = ProductForm()
    return render(request, 'mgt/stocks/list.html', {"stocks": stocks, "form": form})
