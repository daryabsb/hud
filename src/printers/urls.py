

from django.urls import path
from src.printers import views

app_name = 'printers'

urlpatterns = [
    path('export-pdf', views.export_pdf, name='export-pdf'),
]


