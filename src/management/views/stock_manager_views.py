
from django.shortcuts import render
from src.stock.models import Stock

def mgt_stocks(request):
    stocks = Stock.objects.all()
    return render(request, 'mgt/stocks/list.html', {"stocks": stocks})
