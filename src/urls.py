from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from src.core.views import index, not_authorized


def test(request):
    from django.shortcuts import render
    return render(request, 'test.html')


urlpatterns = [
    path('accounts/', include('allauth.urls')),

    path('admin/', admin.site.urls),
    path('not-authorized/', not_authorized, name="not-authorized"),
    path('', index, name="index"),
    path('pos/', include('src.pos.urls'), name="pos"),
    path('mgt/', include('src.management.urls'), name="mgt"),
    path('my-accounts/', include('src.accounts.urls'), name="my-accounts"),
    path('settings/', include('src.configurations.urls'), name="settings"),
    path('finance/', include('src.finances.urls'), name="finances"),

    path('test/', test, name='test')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
