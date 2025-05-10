from django.urls import path
from src.accounts.views import add_new_supplier, customer_profile

app_name = 'accounts'

urlpatterns = [
    path('customers/<slug:slug>/', customer_profile, name='customer-profile'),
    path('add-new-supplier/', add_new_supplier,
                            name='add-new-supplier'),
]