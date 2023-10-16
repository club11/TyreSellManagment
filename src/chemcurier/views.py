from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from . import models
from . import forms
from prices import models as prices_models
from django.views.generic import DetailView, View
import datetime
import pandas as pd

class ChemcourierTableModelDetailView(DetailView):
    model = prices_models.ChemCurierTyresModel
    template_name = 'chemcurier/chemcurier.html'
    
    def get_object(self, queryset=None):
        chemcourier_table = models.ChemCourierTableModel.objects.get_or_create(chemcourier_table='chemcourier_table')[0] 
        
        return chemcourier_table
    
    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')  

        # 1. 
        # 1.1 получить период дат (месяц-год), доступных в спарсенной базе Хим Курьер
        # сфомированно в форме

        #1.2 форма для ввода периорда + получение месяца и года для поиска в базе Chemcurier объектов:
        chosen_year_num = 1
        chosen_year_num = 1
        if forms.INITIAL_PERIOD:                                                            # если пользователь выбрал период
            period_form = forms.PeriodForm(initial={'periods': forms.INITIAL_PERIOD})
            chosen_period = datetime.datetime.strptime(forms.INITIAL_PERIOD, '%Y-%m-%d').date()         
            chosen_year_num = chosen_period.year
            chosen_month_num = chosen_period.month
        else:                                                                               # если пользователь не выбрал период
            period_form = forms.PeriodForm()
            last_period = forms.PERIODS[-1] 
            chosen_period = last_period[0]
            chosen_year_num = chosen_period.year
            chosen_month_num = chosen_period.month  

        context['period_form'] = period_form
        
        # 2 получение типоразмера для отбора (создание формы):
        tyresizes_form = forms.TyreSizeForm()
        context['tyresizes_form'] = tyresizes_form

        tyresize_to_check = None
        if forms.INITIAL_TYREISIZE:
            tyresize_to_check = forms.INITIAL_TYREISIZE
        else:
            if forms.TYRESIZES:
                tyresize_to_check = forms.TYRESIZES[0]      #берем первый из списка

        # 3 получить все объекты химкурьер за исключением нулевых значений (шт. деньги) на дату:

        get_chem_courier_objects_from_base = prices_models.ChemCurierTyresModel.objects.filter(data_month_chem__month=chosen_month_num, data_month_chem__year=chosen_year_num, tyre_size_chem=tyresize_to_check).exclude(average_price_in_usd__isnull=True)      
        get_chem_courier_objects_from_base = get_chem_courier_objects_from_base
        
        
        context['get_chem_courier_objects_from_base'] = get_chem_courier_objects_from_base
        return context  
    
class ChemcourierTableModelUpdateView(View):

    def post(self, request):
        print(request.POST, 'TTTH')
        # 1. получаем период от пользователя для поиска и установки initial значения в дате формы выбора
        get_period = request.POST.get('periods') 
        if get_period:
            forms.INITIAL_PERIOD = get_period
        # 2. получаем типоразмер от пользователя для поиска и установки initial значения в типоразмере формы выбора    
        get_tyresize = request.POST.get('tyresizes') 
        if get_tyresize:
            forms.INITIAL_TYREISIZE = get_tyresize


        return HttpResponseRedirect(reverse_lazy('chemcurier:chemcurier_table'))