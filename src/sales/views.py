from gc import get_objects
from multiprocessing import context
from django.shortcuts import render
from . import forms
from . import models
from django.views.generic import ArchiveIndexView, ListView, DetailView, View
from django.urls import reverse_lazy
from tyres import models as tyres_models
from django.http import HttpResponseRedirect
import datetime

class SalesDetailView(DetailView):
    model = models.SalesTable
    template_name = 'sales/sales.html'

    def get_object(self, queryset=None):
        # получить единственную существующую таблицу SALES. Вся работа в дальнейшем будет осуществляться в ней:
        table_id = self.request.session.get('saled_card_table')
        only_one_exsted_sales_table = models.SalesTable.objects.all()[0]
        sales_table, created  = models.SalesTable.objects.get_or_create(
            pk = only_one_exsted_sales_table.pk,
            defaults={}
        )
        if created:
            self.request.session['saled_card_table'] = sales_table.pk
        ##

        asked_dates = models.PERIOD_UPDATE_SALES                # ВВОДИМЫЕ ПОЛЬЗОВАТЕЛЕМ ДАТЫ ДЛЯ ПОИСКА
        
        if asked_dates:
            list_of_sale_objects = only_one_exsted_sales_table.sales_table.all().filter(date_of_sales__range=asked_dates)    # 2.    все объекты sales в данной таблице SalesTable           # ЗАГЛУШКА
        else:
            list_of_sale_objects = only_one_exsted_sales_table.sales_table.all()
        # 2. получение всех дат:
        #2.1 получение вводимых пользователем датб если нет - то просто все имеющиеся даты:
        if asked_dates:
        #    nad = datetime.datetime.strptime(asked_data, '%Y-%m-%d').date()                        # МОЖЕТ ПРИГОДИТЬСЯ
            list_of_datesfiltered_by_asked_dates = list_of_sale_objects.filter(date_of_sales__range=asked_dates)
            list_of_dates = list(list_of_datesfiltered_by_asked_dates.dates('date_of_sales', 'day'))
        else:   
            list_of_dates = list(list_of_sale_objects.dates('date_of_sales', 'day')) 
        #list_of_dates = list(list_of_sale_objects.dates('date_of_sales', 'day'))           # ЗАГЛУШКА
        models.SALES_DATES = list_of_dates 
                                          
        # 3. FПолучение словаря ШИНА - sales на дату, контрагент                                                         
        list_of_tyre_sales = only_one_exsted_sales_table.table_sales.all() 

        tyre_sales_in_period_dict = {}                                          # Словарь - ШИНА - sales на дату, контрагент
        for obj in list_of_tyre_sales:
            list_sold_on_date = []
            for per in models.SALES_DATES:
                s_p = []
                for sal in obj.tyre.sales.all():
                    if sal.date_of_sales == per and sal.sales_value:
                        date_value = sal.sales_value, sal.date_of_sales, sal.contragent
                        s_p.append(date_value)         
                list_sold_on_date.append(s_p)
            tyre_sales_in_period_dict[obj.tyre] = list_sold_on_date   
        models.SAL_PER_DICTIONARY = tyre_sales_in_period_dict

        ## получение списка контрагентов:                           unique_names_list
        tyre_sal_dict = models.SAL_PER_DICTIONARY
        for obj in list_of_tyre_sales:
            for key, value in tyre_sal_dict.items():
                if obj.tyre == key:
                    contragents_list = []
                    for val in value:
                        for v in val:
                            contragents_list.append(v[2])
            contragents_unique_names_list = list(set(contragents_list)) 
        models.CONTR_UNIQUE_NAME_LIST = contragents_unique_names_list                 
        ##
        ## вызов функции contragents_sale для вывода объемов продаж по контрагентам:
        for contragent in contragents_unique_names_list:
            for obj in list_of_tyre_sales:
                #print(obj.tyre.tyr_sales.all)
                models.CONTRAGENT = contragent
                obj.contragents_sales()

        ##  Расчет словарь итого по каждой шине:
        tyre_sal_total_dict ={}
        for obj in list_of_tyre_sales:
            tyre_sal_total = 0
            if asked_dates:
                #for sal in obj.tyre.sales.all().filter(date_of_sales__range=['2022-09-08', '2022-10-03']):
                for sal in obj.tyre.sales.all().filter(date_of_sales__range=asked_dates):
                    tyre_sal_total += sal.sales_value
                tyre_sal_total_dict[obj] = tyre_sal_total
            else:
                for sal in obj.tyre.sales.all():
                    tyre_sal_total += sal.sales_value
                tyre_sal_total_dict[obj] = tyre_sal_total

        #tyre_sal_total_dict ={}
        #for obj in list_of_tyre_sales:
        #    tyre_sal_total = 0
        #    for sal in obj.tyre.sales.all():
        #        tyre_sal_total += sal.sales_value
        #    tyre_sal_total_dict[obj] = tyre_sal_total
        
        models.TYRE_SAL_TOTAL_DICT = tyre_sal_total_dict
        
        [[obj.sale_on_date(), obj.contragents_sales(), obj.contragents_sales_joined(), obj.total_sale_in_period()] for obj in list_of_tyre_sales] 
        return sales_table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #obj = context.get('object')
        obj = context.get('salestable')
   
        sal_tyr_objects = obj.table_sales.all()
        list_of_sal_tyres = []
        for object in sal_tyr_objects:
            list_of_sal_tyres.append(object)
        list_of_sal_tyres.reverse()
        context['list_objects'] = list_of_sal_tyres
        return context


class SalesTemplateUpdateView(View):
    def post(self, request):
        #print(request.POST, 'TTT')
        #print(self.request.POST.get('change_period'))
        # 1 работа с периодами:
        start_period, end_period = '', ''
        periods_list = []
        for key, value in request.POST.items():
            if key == 'start_period' and value is not '':
                start_period = value
                periods_list.append(start_period)
            elif key == 'end_period' and value is not '':
                end_period = value
                periods_list.append(end_period)
        print(start_period, '||', end_period, 'RAKAKA', periods_list)


        ## 2-й рабочий вариант  (для некоьких групп)
        #tyre_groups_list = request.POST.getlist('tyre_groups')
#
        ## 3 работа с типоразмерами:
        #tyre_sizes_list = []
        #tyre_sizes_list = request.POST.getlist('tyre_sizes')
#
#
        if not periods_list:
            #print('EMPTY periods_list')
            pass
        else:
            models.PERIOD_UPDATE_SALES = periods_list            # передаем в глобальныую данные и перезапускаем страницу
    
        return HttpResponseRedirect(reverse_lazy('sales:sales'))



    