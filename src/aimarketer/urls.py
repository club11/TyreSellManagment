from django.contrib import admin
from django.urls import path, include
from . import views as aimarketer_views
app_name = 'aimarketer'


from .views import TaskView, StartTaskView, TaskStatusView

urlpatterns = [    
    path('aimarketer', aimarketer_views.AiarketerTemplateView.as_view(), name='aimarketer'), 


    path('', TaskView.as_view(), name='task_page'),
    path('start-task/', StartTaskView.as_view(), name='start_task'),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task_status'),

]



