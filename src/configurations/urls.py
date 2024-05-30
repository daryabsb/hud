from django.urls import path
from src.configurations.views import settings_view

app_name = 'configs'

urlpatterns = [
    path('', settings_view, name='settings'),
]
