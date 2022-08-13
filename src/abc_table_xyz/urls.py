from django.contrib import admin
from django.urls import path, include
from . import views as abcxyz_views
app_name = 'abc_table_xyz'

urlpatterns = [    
    path('', abcxyz_views.AbcxyzTemplateView.as_view(), name='main'), 
]