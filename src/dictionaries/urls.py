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

    path('tg_create/', dictionaries_views.TyreGroupCreateView.as_view(), name='tg_create'),  
    path('tg_detail/<int:pk>/', dictionaries_views.TyreGroupDetailView.as_view(), name='tg_detail'), 
    path('tg_update/<int:pk>/', dictionaries_views.TyreGroupUpdateView.as_view(), name='tg_update'), 
    path('tg_delete/<int:pk>/', dictionaries_views.TyreGroupDeleteView.as_view(), name='tg_delete'), 
    path('tg_list/', dictionaries_views.TyreGroupListView.as_view(), name='tg_list'), 

    path('qnt_create/', dictionaries_views.QantityCountCreateView.as_view(), name='qnt_create'),  
    path('qnt_detail/<int:pk>/', dictionaries_views.QantityCountDetailView.as_view(), name='qnt_detail'), 
    path('qnt_update/<int:pk>/', dictionaries_views.QantityCountUpdateView.as_view(), name='qnt_update'), 
    path('qnt_delete/<int:pk>/', dictionaries_views.QantityCountDeleteView.as_view(), name='qnt_delete'), 
    path('qnt_list/', dictionaries_views.QantityCountListView.as_view(), name='qnt_list'), 

    path('curr_create/', dictionaries_views.CurrencyCreateView.as_view(), name='curr_create'),  
    path('curr_detail/<int:pk>/', dictionaries_views.CurrencyDetailView.as_view(), name='curr_detail'), 
    path('curr_update/<int:pk>/', dictionaries_views.CurrencyUpdateView.as_view(), name='curr_update'), 
    path('curr_delete/<int:pk>/', dictionaries_views.CurrencyDeleteView.as_view(), name='curr_delete'), 
    path('curr_list/', dictionaries_views.CurrencyListView.as_view(), name='curr_list'),

    path('contragent_create/', dictionaries_views.ContragentsModelCreateView.as_view(), name='contragent_create'),  
    path('contragent_detail/<int:pk>/', dictionaries_views.ContragentsModelDetailView.as_view(), name='contragent_detail'), 
    path('contragent_update/<int:pk>/', dictionaries_views.ContragentsModelUpdateView.as_view(), name='contragent_update'), 
    path('contragent_delete/<int:pk>/', dictionaries_views.ContragentsModelDeleteView.as_view(), name='contragent_delete'), 
    path('contragent_list/', dictionaries_views.ContragentsModelListView.as_view(), name='contragent_list'), 
]