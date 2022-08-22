from django.contrib import admin
from django.urls import path, include
from . import views as sales_views

app_name = 'sales'

urlpatterns = [    
    path('sales', sales_views.SalesTemplateListView.as_view(), name='sales'), 
]