from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def mgt_home(request):
    context = {
        "modules": [
            {"id": 1, "name": "Products",
                "url": "/mgt/products/", "icon": "shopping-bag"},
            {"id": 2, "name": "Orders", "url": "/mgt/orders/", "icon": "shopping-cart"},
            {"id": 3, "name": "Stock", "url": "/mgt/stocks/",
                "icon": "shopping-basket"},
            {"id": 4, "name": "Printers", "url": "#", "icon": "print"},
            {"id": 5, "name": "Documents", "url": "#", "icon": "newspaper"},
            {"id": 6, "name": "Settings", "url": "#", "icon": "cog"},
            {"id": 7, "name": "Users", "url": "/mgt/users/", "icon": "user"},
        ]
    }
    return render(request, 'mgt/mgt-home.html', context)
