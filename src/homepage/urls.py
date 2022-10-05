from django.urls import path, include
from . import views as homepage_views

app_name = 'homepage'

urlpatterns = [    
    path('', homepage_views.HomeTemplateDetailView.as_view(), name='home'), 
    path('update_home', homepage_views.HomeTemplateUpdateView.as_view(), name='update_home'), 

]