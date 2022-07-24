from django.contrib import admin
from django.urls import path, include
from . import views as filemanagment_views

app_name = 'filemanagment'

urlpatterns = [    
    path('', filemanagment_views.ExcelStaffView.as_view(), name='excel_import'), 
]