from django.contrib import admin
from django.urls import path, include
from . import views as prices_views
app_name = 'prices'

urlpatterns = [    
    path('', prices_views.ComparativeAnalysisTableModelDetailView.as_view(), name='comparative_prices_bel'),
    path('pricestable_update', prices_views.ComparativeAnalysisTableModelUpdateView.as_view(), name='apricestable_update'),

    path('prices_russia', prices_views.ComparativeAnalysisTableModelDetailRussiaView.as_view(), name='comparative_prices_russia'),
    path('prices_russia_update', prices_views.ComparativeAnalysisTableModelRussiaUpdateView.as_view(), name='apricestable_russia_update'),
]