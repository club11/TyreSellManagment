from django.contrib import admin
from django.urls import path, include
from . import views as prices_views
app_name = 'prices'

urlpatterns = [    
    path('', prices_views.ComparativeAnalysisTableModelDetailView.as_view(), name='comparative_prices'),
    path('pricestable_update', prices_views.ComparativeAnalysisTableModelUpdateView.as_view(), name='apricestable_update'),
]