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
    model = models.ChemCourierTableModel
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
        else: 
            try:                                                                               # если пользователь не выбрал период
                period_form = forms.PeriodForm()
                last_period = forms.PERIODS[-1] 
                chosen_period = last_period[0]
                chosen_year_num = chosen_period.year
                chosen_month_num = chosen_period.month  
            except:
                period_form = forms.PeriodForm()
        context['period_form'] = period_form

        # 2 получение типоразмера для отбора (создание формы):
        tyresizes_form = forms.TyreSizeForm()
        tyresize_to_check = None
        if forms.INITIAL_TYREISIZE:
            print('1===', forms.INITIAL_TYREISIZE )
            tyresizes_form = forms.TyreSizeForm(initial={'tyresizes': forms.INITIAL_TYREISIZE})
            tyresize_to_check = forms.INITIAL_TYREISIZE
        else:
            print('2===')
            if forms.TYRESIZES:
                tyresizes_form = forms.TyreSizeForm()
                tyresize_to_check = forms.TYRESIZES[0]      #берем первый из списка    
        context['tyresizes_form'] = tyresizes_form
        context['current_tyresize'] = tyresize_to_check
        # 3 (необязательные)
        # 3.1 получение бренда для отбора (создание формы):
        tyrebrands_to_check = None
        if forms.INITIAL_BRANDS and forms.INITIAL_BRANDS != '-':
            tyrebrands_form = forms.BrandForm(initial={'tyrebrands': forms.INITIAL_BRANDS})
            tyrebrands_to_check = forms.INITIAL_BRANDS
        else:    
            tyrebrands_form = forms.BrandForm()
        context['tyrebrands_form'] = tyrebrands_form
        # 3.2 получение получателя для отбора (создание формы):
        recievers_to_check = None
        if forms.INITIAL_RECIEVER and forms.INITIAL_RECIEVER != '-':
            recievers_form = forms.RecieverForm(initial={'recievers': forms.INITIAL_RECIEVER})
            recievers_to_check = forms.INITIAL_RECIEVER
        else:    
            recievers_form = forms.RecieverForm()
        context['recievers_form'] = recievers_form      
        # 3.3 получение страну производства для отбора (создание формы):
        prod_countrys_to_check = None
        if forms.INITIAL_PRODCOUTRYS and forms.INITIAL_PRODCOUTRYS != '-':
            prod_countrys_form = forms.ProdCountryForm(initial={'prod_countrys': forms.INITIAL_PRODCOUTRYS})
            prod_countrys_to_check = forms.INITIAL_PRODCOUTRYS
        else:    
            prod_countrys_form = forms.ProdCountryForm()
        context['prod_countrys_form'] = prod_countrys_form   

        # 3.4 получение группу для отбора (создание формы):
        prod_groups_to_check = None
        if forms.INITIAL_GROUPS and forms.INITIAL_GROUPS != '-':
            groups_form = forms.GroupForm(initial={'prod_groups': forms.INITIAL_GROUPS})
            prod_groups_to_check = forms.INITIAL_GROUPS
        else:    
            groups_form = forms.GroupForm()
        context['groups_form'] = groups_form   

        # 4 получить все объекты химкурьер за исключением нулевых значений (шт. деньги) на дату:
        get_chem_courier_objects_from_base = prices_models.ChemCurierTyresModel.objects.filter(data_month_chem__month=chosen_month_num, data_month_chem__year=chosen_year_num, tyre_size_chem=tyresize_to_check).exclude(average_price_in_usd__isnull=True)      
        # 4.1 доп. проверки:
        if tyrebrands_to_check:   
            get_chem_courier_objects_from_base = get_chem_courier_objects_from_base.filter(producer_chem=tyrebrands_to_check)
        if recievers_to_check:   
            get_chem_courier_objects_from_base = get_chem_courier_objects_from_base.filter(reciever_chem=recievers_to_check)
        if prod_countrys_to_check:   
            get_chem_courier_objects_from_base = get_chem_courier_objects_from_base.filter(prod_country=prod_countrys_to_check)
        if prod_groups_to_check:   
            get_chem_courier_objects_from_base = get_chem_courier_objects_from_base.filter(group_chem__tyre_group=prod_groups_to_check)

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

        # 3. получаем бренд от пользователя для поиска и установки initial значения в бренде формы выбора    
        get_tyrebrand = request.POST.get('tyrebrands') 
        if get_tyrebrand and get_tyrebrand != '-':
            forms.INITIAL_BRANDS = get_tyrebrand
        else:
            forms.INITIAL_BRANDS = None

        # 4. получаем получателя от пользователя для поиска и установки initial значения в получателях формы выбора    
        get_reciever = request.POST.get('recievers') 
        if get_reciever and get_reciever != '-':
            forms.INITIAL_RECIEVER = get_reciever
        else:
            forms.INITIAL_RECIEVER = None

        # 5. получаем страну производства от пользователя для поиска и установки initial значения в странах производства формы выбора    
        get_prod_countrys = request.POST.get('prod_countrys') 
        if get_prod_countrys and get_prod_countrys != '-':
            forms.INITIAL_PRODCOUTRYS = get_prod_countrys
        else:
            forms.INITIAL_PRODCOUTRYS = None

        # 6. получаем группу производства от пользователя для поиска и установки initial значения в группах формы выбора    
        get_prod_groups = request.POST.get('prod_groups') 
        if get_prod_groups and get_prod_groups != '-':
            forms.INITIAL_GROUPS = get_prod_groups
        else:
            forms.INITIAL_GROUPS = None

        return HttpResponseRedirect(reverse_lazy('chemcurier:chemcurier_table'))


