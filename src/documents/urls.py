from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.documents.api.views import DocumentViewSet, document_columns_view

from src.documents import views

router = DefaultRouter()
router.register('list', DocumentViewSet, basename='api-list')

app_name = 'documents'


urlpatterns = [
    path('', views.document_list_view, name='documents-list-view'),
    path('list/', views.document_list, name='documents-list'),
    path('documents-json/', views.DocumentJsonView.as_view(), name='documents-json'),
]


urlpatterns += [
    path('api/', include(router.urls)),
    path('api/document-columns/', document_columns_view, name='document-columns'),
]


[
    'APIRootView', 'APISchemaView', 'SchemaGenerator', 
    'default_schema_renderers', 'get_api_root_view', 'get_default_basename', 'get_lookup_regex', 
    'get_method_map', 'get_routes', 'get_urls', 'include_format_suffixes', 'include_root_view', 
    'register', 'registry', 'root_renderers', 'root_view_name', 'routes', 'trailing_slash', 'urls'
    ]