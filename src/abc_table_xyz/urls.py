from django.contrib import admin
from django.urls import path, include
from . import views as abcxyz_views
app_name = 'abc_table_xyz'

urlpatterns = [    
    #path('', abcxyz_views.AbcxyzTemplateDetailView.as_view(), name='abc'),
    path('', abcxyz_views.AbcxyzTemplateDetailView.as_view(), name='abctable'),
    path('abctable_update', abcxyz_views.ABCXYZTemplateUpdateView.as_view(), name='abctable_update'),
     
    #path('<int:pk>/', abcxyz_views.AbcxyzTemplateDetailView.as_view(), name='abctable'),  
]