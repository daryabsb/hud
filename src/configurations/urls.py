from django.urls import path
from src.configurations.views import settings_view, update_config

app_name = 'configs'

urlpatterns = [
    path('', settings_view, name='settings'),
    path('update/<int:id>', update_config, name='update-settings'),
]
