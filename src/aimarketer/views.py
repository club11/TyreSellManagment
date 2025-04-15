
from django.shortcuts import render
from django.views.generic import FormView#, TemplateView,
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
#from celery.result import AsyncResult
import prices.models
import chemcurier.models

class AiarketerTemplateView(FormView):
    #model = models.SalesTable
    template_name = 'aimarketer/aimarketer.html'
    form_class = forms.AIForm

    #@app.task
    @shared_task
    #def open_ai_reload_paige(request, context):
    def open_ai_reload_paige(a_request):    
    #def open_ai_reload_paige(self):    
        print('ASS')
        a_request
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
              "content": a_request
            }
          ]
        )
        print('****+++++++++++++++++++++++++++++++++++', completion.choices[0].message.content)
        #context = self.get_context_data(**kwargs)
        #a_context['response'] = completion.choices[0].message.content
        return completion.choices[0].message.content
        #return render(a_request, 'aimarketer/aimarketer.html', context=a_context)
 
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # 1. вариант - ответ AI- по тестовому запросу:
        if self.request.POST.get('ai_request'):
            data_to_analyse = request.POST['ai_request']
        # 2. вариант - анализ данных из BD:    
        #else:
            a_queryset = prices.models.ChemCurierTyresModel.objects.all()[:30].values_list() #.values_list('tyre_size_chem', 'producer_chem', 'val_on_moth_chem')
            #print('AAA=============================', a_queryset)
            # Форматируем данные для анализа
        # 2. Подготовка структурированных данных
            
            from django.core.serializers.json import DjangoJSONEncoder
            data_to_analyse_data = json.dumps(list(a_queryset), cls=DjangoJSONEncoder)
            #print(data_to_analyse)
       
        # 5. Формирование промпта для AI
            data_to_analyse_is = f"""
            Задачи анализа:
            1. Выявить топ-10 брендов по объему импорта 
            2. Выявить топ-10 типоразмеров по объему импорта
            в следующих данных:
            {data_to_analyse_data}
            """
            # 3. Проанализировать распределение по странам производства
            # 4. Найти аномалии в данных
            # 5. Определить корреляцию между типоразмером и ценой
            # 6. Спрогнозировать спрос на следующие 6 месяцев
       
            print('WHAT WE ANALYZE', data_to_analyse)

            self.open_ai_reload_paige.delay(data_to_analyse)
            #self.open_ai_reload_paige.delay(data_to_analyse_data)
            self.open_ai_reload_paige.delay(data_to_analyse_is)

        return render(self.request, 'aimarketer/aimarketer.html', context=context)
    
    

