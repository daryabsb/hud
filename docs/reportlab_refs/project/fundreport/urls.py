from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from project.fundreport import views

urlpatterns = []

urlpatterns.extend([
    # This URL serves the index page:
    path('', views.index,),

    # This URL accepts a fund ID and generates 
    # the corresponding PDF
    path('fundreport/<int:id>.pdf', views.fundreport),
])
