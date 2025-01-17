from django.urls import path

from src.payments.views import (
    save_pos_payment, order_payment_change
)

app_name = "payments"


urlpatterns = [
    path('save-payment/<str:order_number>/',
         save_pos_payment, name='save-payment'),
    path('payment-change/<str:order_number>/',
         order_payment_change, name='change'),
]
