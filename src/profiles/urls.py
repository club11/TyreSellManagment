from django.contrib import admin
from django.urls import path, include
from . import views as profiles_views

app_name = 'profiles'


urlpatterns = [    
    path('register', profiles_views.RegisterFormView.as_view(), name='register'),

]