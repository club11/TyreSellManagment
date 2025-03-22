
from django.shortcuts import render
from django.views.generic import FormView, RedirectView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from . import forms
#from . import models
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from proj.celery import app

from celery import shared_task
from celery.result import AsyncResult

#@app.task
@shared_task
def open_ai_reload_paige(a_request):         
    some_request = a_request
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key="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",
    )
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
      },
      extra_body={},
      model="deepseek/deepseek-r1-zero:free", 
      messages=[
        {
          "role": "user",
          "content": some_request
        }
      ]
    )
    print('****', completion.choices[0].message.content)
    #a_context = super().get_context_data(**kwargs)
    #a_context = context
    #a_context['response'] = completion.choices[0].message.content
    return completion.choices[0].message.content


################
import time
@shared_task(bind=True)
def long_running_task(self, duration=10):
    """Имитация длительной задачи с прогрессом"""
    for i in range(duration):
        time.sleep(1)
        self.update_state(
            state='PROGRESS',
            meta={'current': i+1, 'total': duration}
        )
    return {'result': 'Завершено успешно!', 'details': f'Обработано {duration} итераций'}

class AiarketerTemplateView(FormView):
    template_name = 'aimarketer/aimarketer.html'
    form_class = forms.AIForm

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #print(self.request.POST, 'DODGE================')
        if self.request.POST.get('ai_request'):
            task = self.open_ai_reload_paige.delay(request.POST['ai_request'])
            #self.request.session['task_id'] = task.id

            return JsonResponse({'task_id': task.id}, status=202)
        return render(self.request, 'aimarketer/aimarketer.html', context=context) 
class TaskView(TemplateView):
    template_name = 'task_page.html'

class StartTaskView(TemplateView):
    def get(self, request, *args, **kwargs):
        task = long_running_task.delay(10)  # Запуск задачи на 10 секунд
        return JsonResponse({'task_id': task.id}, status=202)
class TaskStatusView(TemplateView):
    def get(self, request, task_id, *args, **kwargs):
        task = long_running_task.AsyncResult(task_id)
        
        if task.state == 'FAILURE':
            return JsonResponse({'status': 'error', 'error': str(task.result)})   
        response = {
            'status': task.state,
            'task_id': task_id
        }  
        if task.state == 'PROGRESS':
            response.update({
                'progress': task.info.get('current', 0),
                'total': task.info.get('total', 10)
            })     
        if task.state == 'SUCCESS':
            response['result'] = task.result
        
        return JsonResponse(response)
################    

