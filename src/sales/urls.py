from django.contrib import admin
from django.urls import path, include
from . import views as sales_views

app_name = 'sales'

urlpatterns = [    
    #path('sales', sales_views.SalesTemplateListView.as_view(), name='sales'), 
    path('sales', sales_views.SalesDetailView.as_view(), name='sales'), 
    path('update_sales', sales_views.SalesTemplateUpdateView.as_view(), name='update_sales'), 
]