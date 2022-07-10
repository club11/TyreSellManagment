from django.contrib import admin
from django.urls import path, include
from . import views as dictionaries_views

app_name = 'dictionaries'

urlpatterns = [    
    path('dictionaries/', dictionaries_views.DictionariesTemplateView.as_view(), name='dictionaries'), 

    path('ts_create/', dictionaries_views.TyreSizCreateView.as_view(), name='ts_create'),  
    path('ts_detail/<int:pk>/', dictionaries_views.TyreSizeDetailView.as_view(), name='ts_detail'), 
    path('ts_update/<int:pk>/', dictionaries_views.TyreSizeUpdateView.as_view(), name='ts_update'), 
    path('ts_delete/<int:pk>/', dictionaries_views.TyreSizeDeleteView.as_view(), name='ts_delete'), 
    path('ts_list/', dictionaries_views.TyreSizeListView.as_view(), name='ts_list'), 

    path('model_create/', dictionaries_views.ModelNameCreateView.as_view(), name='model_create'),  
    path('model_detail/<int:pk>/', dictionaries_views.ModelNameDetailView.as_view(), name='model_detail'), 
    path('model_update/<int:pk>/', dictionaries_views.ModelNameUpdateView.as_view(), name='model_update'), 
    path('model_delete/<int:pk>/', dictionaries_views.ModelNameDeleteView.as_view(), name='model_delete'), 
    path('model_list/', dictionaries_views.ModelNameListView.as_view(), name='model_list'), 
]