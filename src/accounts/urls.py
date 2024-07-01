from django.urls import path
from src.accounts.views import add_new_supplier

app_name = 'accounts'

urlpatterns = [
    path('add-new-supplier/', add_new_supplier,
                            name='add-new-supplier'),
]