from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from src.core.views import index, not_authorized
from django.shortcuts import redirect, render
from src.accounts.models import User
from django.contrib.auth.decorators import login_required
import src.routing as routing  # We’ll create this

from src.configurations.models import ApplicationProperty
from src.core.views import search_datatable


def test(request):
    return render(request, 'test.html')


def load_window(request):
    user = request.user

    print('Window loaaded, render the password window!')
    return render(request, 'partials/warning-toaster.html')


@login_required
def submit_password(request):
    email = request.GET.get('email', None)
    if email:
        current_user = ApplicationProperty.objects.get(name='email')
        # current_user.value =
        print(current_user)
    else:
        print("No email provided!!!")
    return render(request, 'buttons/password-confirm.html', {'success': False})


@login_required
def confirm_pin(request):
    pin = request.GET.get('pin', None)
    current_user = None

    user_pin = request.user.pin
    if pin and int(pin) == user_pin:
        return render(request, 'buttons/password-confirm.html', {'success': True})
    return render(request, 'buttons/password-confirm.html', {'success': False})


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('load-password-window/', load_window, name="not-authorized"),
    path('enter-pin/', confirm_pin, name='enter-pin'),
    path('submit-password/', submit_password, name='submit-password'),

    path('admin/', admin.site.urls),
    path('not-authorized/', not_authorized, name="not-authorized"),
    path('', index, name="index"),
    path('search-datatable/<str:app_name>/<str:model>/',
         search_datatable, name="search-datatable"),
    path('pos/', include('src.pos.urls'), name="pos"),
    path('payments/', include('src.payments.urls'), name="payments"),
    path('mgt/', include('src.management.urls'), name="mgt"),
    path('my-accounts/', include('src.accounts.urls'), name="my-accounts"),
    path('settings/', include('src.configurations.urls'), name="settings"),
    path('finance/', include('src.finances.urls'), name="finances"),
    path('printers/', include('src.printers.urls'), name="printers"),
    path('documents/', include('src.documents.urls'), name="documents"),
    path('orders/', include('src.orders.urls'), name="orders"),
    path('products/', include('src.products.urls'), name="products"),
    path('stock/', include('src.stock.urls'), name="stock"),
    path('game/', include('src.games.urls'), name="games"),

    path('test/', test, name='test'),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # urlpatterns += debug_toolbar_urls()

websocket_urlpatterns = routing.websocket_urlpatterns