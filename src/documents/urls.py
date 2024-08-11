from django.urls import path

from src.documents import views

app_name = 'documents'


urlpatterns = [
    path('', views.document_list_view, name='documents-list'),
    path('documents-json/', views.DocumentJsonView.as_view(), name='documents-json'),
]