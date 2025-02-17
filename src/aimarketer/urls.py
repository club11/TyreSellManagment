from django.contrib import admin
from django.urls import path, include
from . import views as aimarketer_views
app_name = 'aimarketer'

urlpatterns = [    
    path('aimarketer', aimarketer_views.AiarketerTemplateView.as_view(), name='aimarketer'), 

]