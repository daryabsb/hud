from django.shortcuts import render




def pos_home(request, nunmber=None):
    context = {}
    return render(request, 'cotton/pos/home/index.html', context)
