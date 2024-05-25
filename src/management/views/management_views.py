from django.shortcuts import render


def mgt_home(request):
    context = {
        "modules": [
            {"id": 1, "name": "Products", "url": "/mgt/products/", "icon": "shopping-bag"},
            {"id": 2, "name": "Orders", "url": "#", "icon": "shopping-cart"},
            {"id": 3, "name": "Stock", "url": "#", "icon": "shopping-basket"},
            {"id": 4, "name": "Printers", "url": "#", "icon": "print"},
            {"id": 5, "name": "Documents", "url": "#", "icon": "newspaper"},
            {"id": 6, "name": "Settings", "url": "#", "icon": "cog"},
        ]
    }
    return render(request, 'mgt/mgt-home.html', context)