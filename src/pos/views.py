from django.shortcuts import render

# Create your views here.


def pos_home(request):
    return render(request, 'pos/pos-home.html')

