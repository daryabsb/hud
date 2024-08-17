from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.documents.api.views import DocumentViewSet

from src.documents import views

router = DefaultRouter()
router.register('list', DocumentViewSet)


app_name = 'documents'


urlpatterns = [
    path('', views.document_list_view, name='documents-list'),
    path('documents-json/', views.DocumentJsonView.as_view(), name='documents-json'),
]


urlpatterns = [
    path('api/', include(router.urls)),
]