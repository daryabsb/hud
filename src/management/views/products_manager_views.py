from django.shortcuts import render
from src.products.models import Product
# Create your views here.


def mgt_products(request):
    products = Product.objects.all()
    return render(request, 'mgt/products/list.html', {"products": products})