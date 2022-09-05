from django.urls import path, include
from . import views as homepage_views

app_name = 'homepage'

urlpatterns = [    
    path('', homepage_views.HomeTemplateDetailView.as_view(), name='home'), 
    #path('', homepage_views.HomeTemplateListView.as_view(), name='home'), 


]