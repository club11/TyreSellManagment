from django.contrib import admin
from django.urls import path, include
from . import views as tyres_views

app_name = 'tyres'

urlpatterns = [    

    path('tyre_card_create/', tyres_views.TyreCardCreateView.as_view(), name='tyre_card_create'),  
    path('tyre_card_detail/<int:pk>/', tyres_views.TyreCardDetailView.as_view(), name='tyre_card_detail'), 
    path('tyre_card_update/<int:pk>/', tyres_views.TyreCardUpdateView.as_view(), name='tyre_card_update'), 
    path('tyre_card_delete/<int:pk>/', tyres_views.TyreCardDeleteView.as_view(), name='tyre_card_delete'), 
    path('tyre_card_list/', tyres_views.TyreCardListView.as_view(), name='tyre_card_list'), 

    path('tyre_create/', tyres_views.TyreCreateView.as_view(), name='tyre_create'),  
    #path('tyre_detail/<int:pk>/', tyres_views.TyreDetailView.as_view(), name='tyre_detail'), 
    path('tyre_update/<int:pk>/', tyres_views.TyreUpdateView.as_view(), name='tyre_update'), 
    path('tyre_delete/<int:pk>/', tyres_views.TyreDeleteView.as_view(), name='tyre_delete'), 
    path('tyre_list/', tyres_views.TyreListView.as_view(), name='tyre_list'), 
]