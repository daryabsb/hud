from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_page, name='game_page'),
    path('guess/', views.guess_letter, name='guess_letter'),
]
