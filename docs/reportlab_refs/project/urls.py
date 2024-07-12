from django.urls import include, path
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = []


urlpatterns.extend ([
    
    # Main site
    path('', include('project.fundreport.urls')),

    #admin
    path('admin/', admin.site.urls),

])
