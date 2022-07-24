from django.contrib import admin
from django.urls import path, include

from unicodedata import name
from django.conf import settings
from django.conf.urls.static import static
from dictionaries import views as dictionaries_views

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dictionaries_views.HomeTemplateView.as_view(), name='home'),  
    path('directory/', include('dictionaries.urls', namespace='dictionaries')), 
    path('tyre/', include('tyres.urls', namespace='tyres')),
    path('filemanagment/', include('filemanagment.urls', namespace='filemanagment')),      
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
