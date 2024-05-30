from django.shortcuts import render

# Create your views here.


def settings_view(request):
    return render(request, 'config/index.html')
