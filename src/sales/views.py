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
from tyres import models as tyre_models
from dictionaries import models as dictionaries_models

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
        #2.1 получение вводимых пользователем дат ФИЛЬТР 1. если нет UPDATEVIEW  - то просто все имеющиеся даты:
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
        ###print( 'GGG1', list_of_tyre_sales)

        ## ФИЛЬТР 2-й рабочий вариант  (для некоьких групп) UPDATEVIEW по группе шин
        if models.TYRE_GROUP_NAMES:
            tyre_groups_for_table = []
            tyre_groups_for_table = models.TYRE_GROUP_NAMES
            list_of_tyre_sales = list_of_tyre_sales.filter(tyre__tyre_group__tyre_group__in=tyre_groups_for_table)
            ###print(tyre_groups_for_table, 'GGG2', list_of_tyre_sales)

        # ФИЛЬТР 3  - задаваемые типоразмеры шин для работы в таблице:
        if models.TYRE_GROUP_SIZES:
            tyre_sizes_for_table = []
            tyre_sizes_for_table = models.TYRE_GROUP_SIZES
            list_of_tyre_sales = list_of_tyre_sales.filter(tyre__tyre_size__tyre_size__in=tyre_sizes_for_table)
            #print(tyre_sizes_for_table, 'GGG3', list_of_tyre_sales)

        # ФИЛЬТР 4  - задаваемые модели шин для работы в таблице:
        if models.TYRE_GROUP_MODELS:
            tyre_models_for_table = []
            tyre_models_for_table = models.TYRE_GROUP_MODELS
            list_of_tyre_saless = list_of_tyre_sales.filter(tyre__tyre_model__model__in=tyre_models_for_table)
        #print(tyre_models_for_table, 'GGG4', list_of_tyre_sales)

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
  
        models.TYRE_SAL_TOTAL_DICT = tyre_sal_total_dict
        [[obj.sale_on_date(), obj.contragents_sales(), obj.contragents_sales_joined(), obj.total_sale_in_period()] for obj in list_of_tyre_sales] 
        return sales_table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #obj = context.get('object')
        obj = context.get('salestable')
   
        #sal_tyr_objects = obj.table_sales.all()
        #list_of_sal_tyres = []
        #for object in sal_tyr_objects:
        #    list_of_sal_tyres.append(object)
        #list_of_sal_tyres.reverse()
        #print('list_of_sal_tyres', list_of_sal_tyres)
        #context['list_objects'] = list_of_sal_tyres

        # 2  группа шин:
        tyre_groups = dictionaries_models.TyreGroupModel.objects.all()
        tyre_groups_list = []
        for group_name in tyre_groups:
            tyre_groups_list.append(group_name.tyre_group)
        context['tyre_groups'] = tyre_groups_list

        listtyr_home_ojects_filtered = []                   ############## !!!!!!!!!!!!!!!!!!!!!
        if models.TYRE_GROUP_NAMES:
            tyres_list = tyre_models.Tyre.objects.all()
            object = context.get('object')
            # ВЫВОД ОТФИЛЬТРОВАННЫХ TYRES_HOME группа шин:
            listtyr_home_ojects_filtered = []
            if models.TYRE_GROUP_NAMES:
                tyre_groups_for_table = []
                tyre_groups_for_table = models.TYRE_GROUP_NAMES
                tyres_list = tyres_list.filter(tyre_group__tyre_group__in=tyre_groups_for_table)

                sal_tyr_objects = obj.table_sales.all()
                for obj in sal_tyr_objects:
                    for tyr in tyres_list: 
                        if obj.tyre == tyr:
                            listtyr_home_ojects_filtered.append(obj)
                context['list_objects'] = listtyr_home_ojects_filtered
        else:                                                                                       # здеся просто вывод всех шин . всех-всех
            sal_tyr_objects = obj.table_sales.all()
            list_of_sal_tyres = []
            for object in sal_tyr_objects:
                list_of_sal_tyres.append(object)
            list_of_sal_tyres.reverse()
            context['list_objects'] = list_of_sal_tyres
            ###

        #######################################################################################
        ## 3 типоразмер:
        tyre_sizes = dictionaries_models.TyreSizeModel.objects.all()
        tyre_sizes_list = []
        for tyre_sizes_name in tyre_sizes:
            tyre_sizes_list.append(tyre_sizes_name.tyre_size)
        context['tyre_sizes'] = tyre_sizes_list
        
        # ВЫВОД ОТФИЛЬТРОВАННЫХ TYRES_HOME типорапзмер:
        if listtyr_home_ojects_filtered:                    # если фильтруется еще по группам шин:
            tyre_sizes_for_table = []
            tyre_sizes_for_table = models.TYRE_GROUP_SIZES
            tyres_list = tyres_list.filter(tyre_size__tyre_size__in=tyre_sizes_for_table)
            #print('tyres_lis', tyres_list)

            if tyre_sizes_for_table:
                tyres_list = tyres_list.filter(tyre_size__tyre_size__in=tyre_sizes_for_table)
                listtyr_home_ojects_filtered = []
                for obj in sal_tyr_objects:
                    for tyr in tyres_list: 
                        if obj.tyre == tyr:
                            listtyr_home_ojects_filtered.append(obj)
                context['list_objects'] = listtyr_home_ojects_filtered
        else:                                               # если фильтруется еще без групп шин:
            tyres_list = tyre_models.Tyre.objects.all()
            tyre_sizes_for_table = []
            tyre_sizes_for_table = models.TYRE_GROUP_SIZES
            tyres_list = tyres_list.filter(tyre_size__tyre_size__in=tyre_sizes_for_table)
            if tyre_sizes_for_table:
                tyres_list = tyres_list.filter(tyre_size__tyre_size__in=tyre_sizes_for_table)
                listtyr_home_ojects_filtered = []
                for obj in sal_tyr_objects:
                    for tyr in tyres_list: 
                        if obj.tyre == tyr:
                            listtyr_home_ojects_filtered.append(obj)
                context['list_objects'] = listtyr_home_ojects_filtered
        #################################################################################################

        ## 4 модель:
        tire_models = dictionaries_models.ModelNameModel.objects.all()
        tyre_models_list = []
        for tyre_model_name in tire_models:
            tyre_models_list.append(tyre_model_name.model)
        context['tyre_models'] = tyre_models_list

        # ВЫВОД ОТФИЛЬТРОВАННЫХ TYRES_HOME модель:
        if listtyr_home_ojects_filtered:                    # если фильтруется еще по группам шин:
            tyre_models_for_table = []
            tyre_models_for_table = models.TYRE_GROUP_MODELS
            tyres_list = tyres_list.filter(tyre_model__model__in=tyre_models_for_table)
            #print('tyres_lis', tyres_list)

            if tyre_models_for_table:
                tyres_list = tyres_list.filter(tyre_model__model__in=tyre_models_for_table)
                listtyr_home_ojects_filtered = []
                for obj in sal_tyr_objects:
                    for tyr in tyres_list: 
                        if obj.tyre == tyr:
                            listtyr_home_ojects_filtered.append(obj)
                context['list_objects'] = listtyr_home_ojects_filtered
        else:                                               # если фильтруется еще без групп шин:
            tyres_list = tyre_models.Tyre.objects.all()
            tyre_models_for_table = []
            tyre_models_for_table = models.TYRE_GROUP_MODELS
            tyres_list = tyres_list.filter(tyre_model__model__in=tyre_models_for_table)
            if tyre_models_for_table:
                tyres_list = tyres_list.filter(tyre_model__model__in=tyre_models_for_table)
                listtyr_home_ojects_filtered = []
                for obj in sal_tyr_objects:
                    for tyr in tyres_list: 
                        if obj.tyre == tyr:
                            listtyr_home_ojects_filtered.append(obj)
                context['list_objects'] = listtyr_home_ojects_filtered

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
        #print(start_period, '||', end_period, 'RAKAKA', periods_list)


        # 2-й рабочий вариант  (для некоьких групп)
        tyre_groups_list = request.POST.getlist('tyre_groups')

        # 3 работа с типоразмерами:
        tyre_sizes_list = []
        tyre_sizes_list = request.POST.getlist('tyre_sizes')

        # 4 работа с моделями
        tyre_models_list = []
        tyre_models_list = request.POST.getlist('tyre_models')

        if not periods_list:
            #print('EMPTY periods_list')
            pass
        else:
            models.PERIOD_UPDATE_SALES = periods_list            # передаем в глобальныую данные и перезапускаем страницу

        if not tyre_groups_list:
            #print('EMPTY tyre_groups_list')
            pass
        else:
            models.TYRE_GROUP_NAMES = tyre_groups_list 
            #print(models.TYRE_GROUP_NAMES, 'models.TYRE_GROUP_NAMES', 'ITOGO')     

        if not tyre_sizes_list:
            #print('EMPTY tyre_sizes_list')
            pass
        else:
            models.TYRE_GROUP_SIZES = tyre_sizes_list       

        if not tyre_models_list:
            #print('EMPTY tyre_sizes_list')
            pass
        else:
            models.TYRE_GROUP_MODELS = tyre_models_list
    
        return HttpResponseRedirect(reverse_lazy('sales:sales'))



    