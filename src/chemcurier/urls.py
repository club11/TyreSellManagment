from django.contrib import admin
from django.urls import path, include
from . import views as chemcurier_views
app_name = 'chemcurier'


urlpatterns = [    
    path('', chemcurier_views.ChemcourierTableModelDetailView.as_view(), name='chemcurier_table'),
    path('chemcurier_update', chemcurier_views.ChemcourierTableModelUpdateView.as_view(), name='chemcurier_update'),
    path('chemcurier_progressive', chemcurier_views.ChemcourierProgressiveTableModelDetailView.as_view(), name='chemcurier_table_progressive'),
    path('chemcurier_update_progressive', chemcurier_views.ChemcourierTableProgressiveModelUpdateView.as_view(), name='chemcurier_update_progressive'),

]


#urlpatterns = [    
#    path('', prices_views.ComparativeAnalysisTableModelDetailView.as_view(), name='comparative_prices_bel'),
#    path('pricestable_update', prices_views.ComparativeAnalysisTableModelUpdateView.as_view(), name='apricestable_update'),
#
#    path('prices_russia', prices_views.ComparativeAnalysisTableModelDetailRussiaView.as_view(), name='comparative_prices_russia'),
#    path('prices_russia_update', prices_views.ComparativeAnalysisTableModelRussiaUpdateView.as_view(), name='apricestable_russia_update'),
#]