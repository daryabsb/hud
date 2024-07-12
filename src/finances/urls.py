
from django.urls import path
from src.finances import views


app_name = 'finance'

urlpatterns = [
    path('', views.index,),
    path('<int:id>.pdf', views.fundreport),
]
