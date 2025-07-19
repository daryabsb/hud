from django.urls import path, include
from src.pos2 import views

app_name = "pos2"

urlpatterns = [
    path('', views.pos_home, name='pos-home'),
    path('<str:number>/', views.pos_order, name='pos-order'),
]