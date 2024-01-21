from django.contrib import admin
from django.urls import path, include

from unicodedata import name
from django.conf import settings
from django.conf.urls.static import static
from dictionaries import views as dictionaries_views
from profiles import views as profiles_views
#from django.contrib.auth import views as auth_views #login logout etc.

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('homepage/', include('homepage.urls', namespace='home')), 
    path('directory/', include('dictionaries.urls', namespace='dictionaries')), 
    path('tyre/', include('tyres.urls', namespace='tyres')),
    path('filemanagment/', include('filemanagment.urls', namespace='filemanagment')),      
    path('abctable/', include('abc_table_xyz.urls', namespace='abctable')),   
    path('sales/', include('sales.urls', namespace='sales')),  
    path('prices/', include('prices.urls', namespace='prices')),  
    path('chemcurier/', include('chemcurier.urls', namespace='chemcurier')),  
    path('profiles/', include('profiles.urls', namespace='profiles')), 


    
    path('login', profiles_views.SomeUserLoginView.as_view(), name='login'),
    path('chp', profiles_views.SomePasswordChangeView.as_view(), name='chp'),
    path('logged_out', profiles_views.SomeLogoutView.as_view(), name='logged_out'),
#    path('login', auth_views.LoginView.as_view(), name='login'),



] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
