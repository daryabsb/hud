
from django.urls import path
from src.pos.views import (
    pos_home,
)
app_name="pos"

urlpatterns = [
    path('', pos_home, name='pos-home'),
]