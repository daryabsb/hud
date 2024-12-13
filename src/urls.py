from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from src.core.views import index, not_authorized
from django.shortcuts import render
from src.accounts.models import User


def test(request):
    return render(request, 'test.html')


def load_window(request):
    user = request.user

    print('Window loaaded, render the password window!')
    return render(request, 'partials/warning-toaster.html')


def confirm_pin(request):
    pin = request.GET.get('pin', None)
    user_pin = request.user.pin
    if pin and int(pin) == user_pin:
        return render(request, 'buttons/password-confirm.html', {'success': True})
    return render(request, 'buttons/password-confirm.html', {'success': False})


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('load-password-window/', load_window, name="not-authorized"),
    path('enter-pin/', confirm_pin, name='enter-pin'),

    path('admin/', admin.site.urls),
    path('not-authorized/', not_authorized, name="not-authorized"),
    path('', index, name="index"),
    path('pos/', include('src.pos.urls'), name="pos"),
    path('mgt/', include('src.management.urls'), name="mgt"),
    path('my-accounts/', include('src.accounts.urls'), name="my-accounts"),
    path('settings/', include('src.configurations.urls'), name="settings"),
    path('finance/', include('src.finances.urls'), name="finances"),
    path('printers/', include('src.printers.urls'), name="printers"),
    path('documents/', include('src.documents.urls'), name="documents"),
    path('game/', include('src.games.urls'), name="games"),

    path('test/', test, name='test')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
