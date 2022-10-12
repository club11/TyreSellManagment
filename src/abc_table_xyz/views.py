from datetime import date
from multiprocessing import context
from multiprocessing.resource_sharer import stop
from pickletools import anyobject
from pyexpat import model
from django.shortcuts import render
from . import models
from tyres import models as tyres_models
from sales import models as sales_models
from django.views.generic import TemplateView, DetailView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from tyres import models as tyre_models
from dictionaries import models as dictionaries_models
import collections

from tyres import models as tyre_model
### работа с датами:
import calendar
from datetime import datetime, timedelta
import pandas
###

class AbcxyzTemplateDetailView(DetailView):
    model = models.AbcxyzTable
    template_name = 'abc_table_xyz/abc.html'
    #login_url = reverse_lazy('abc_table_xyz:abctable')

    def get_object(self, queryset=None):                
        # get abc_table
        table_id = self.request.session.get('table_id')             
        abc_table, created = models.AbcxyzTable.objects.get_or_create(         
        pk=table_id,                                       
        defaults={},
        )
        if created:
            self.request.session['table_id'] = abc_table.pk
            all_tyres = list(tyres_models.Tyre.objects.all())
            for n in all_tyres:
                models.Abcxyz.objects.bulk_create([models.Abcxyz(tyre=n, table=abc_table)])
            list_of_abc_bjects = models.Abcxyz.objects.all()

            for obj in list_of_abc_bjects:
                tyre_sales_all = sales_models.Sales.objects.filter(tyre=obj.tyre)
                obj.sales.set(tyre_sales_all)
                
        list_of_abc_bjects = abc_table.table.all()          # ПЕРЕЧЕЬ ВСЕХ ОБЪЕКТОВ Abcxyz
        total_sales_in_period = {}                          # объем продаж шины за период всего: 
        tyre_total_price = 0                                # объем продаж всех шин за период всего: 
        period_dict_final = {}                              # ИТОГОВЫЙ СЛОВАРЬ для формирования (отрисовки) в таблице: ПЕРИОД - ОБЩИЙ ОБЪЕМ ПРОДАЖ ЗА ДАННЫЙ ПЕРИОД для конкретной шины
        tyre_percent_in_total_amount = {}                   # доля шины в общем объеме продаж за период
        sorted_tyres_dict_final = {}                        # словарь ключ - pk объекта, значения - позиция в очереди, значение (объем продаж), доля в общем объеме, доля в общем объеме с накопмительным итогом  ### ТАК МОЖЕТ ТУТ ДАЖЕ ДАННЫЕ ИЗЛИШНИЕ
        average_revenue = {}                                # средне - периодная выручка
        dict_list_sales_on_period_final = {}                # сортировка sales по числам  и формирование финального словаря ключ = число год месяц , значения = объекты sales
        #tyre_sales_sold_in_small_period = {}               # ключ объект Abcxyz и дата продажи. значение - объекты Sales. ДЛЯ ОТРИСОВКИ ПРОДАЖ ПО МАЛЫМ ПЕРИОДАМ ПО КОНКРЕТНОЙ ШИНЕ
        unique_keys = []                                    # даты продаж 


        # ФИЛЬТР 1 - задаваемый период продаж для работы в таблице:
        sales_period_for_table = models.PERIOD_UPDATE_SALES  

        ##  
        ## ФИЛЬТР 2-й рабочий вариант  (для некоьких групп) UPDATEVIEW по группе шин
        if models.TYRE_GROUP_NAMES:
            tyre_groups_for_table = []
            tyre_groups_for_table = models.TYRE_GROUP_NAMES
            list_of_abc_bjects = list_of_abc_bjects.filter(tyre__tyre_group__tyre_group__in=tyre_groups_for_table)
            #print(list_of_abc_bjects, 'GGG2', list_of_abc_bjects)

        # ФИЛЬТР 3  - задаваемые типоразмеры шин для работы в таблице:
        if models.TYRE_GROUP_SIZES:
            tyre_sizes_for_table = []
            tyre_sizes_for_table = models.TYRE_GROUP_SIZES
            list_of_abc_bjects = list_of_abc_bjects.filter(tyre__tyre_size__tyre_size__in=tyre_sizes_for_table)
            #print(list_of_abc_bjects, 'GGG3', list_of_abc_bjects)

        # ФИЛЬТР 4  - задаваемые модели шин для работы в таблице:
        if models.TYRE_GROUP_MODELS:
            tyre_models_for_table = []
            tyre_models_for_table = models.TYRE_GROUP_MODELS
            list_of_abc_bjects = list_of_abc_bjects.filter(tyre__tyre_model__model__in=tyre_models_for_table)
        #print(list_of_abc_bjects, 'GGG4', list_of_abc_bjects)
        

        # 1 расчет объемов продаж шины за период всего:     (ДОРАБОТАТЬ ПО ПЕРИОДАМ)                                  
        for obj in list_of_abc_bjects:
            total_sales = 0 
            if sales_period_for_table:
                for sale in obj.sales.all().filter(date_of_sales__range=sales_period_for_table):
                    val = sale.sales_value
                    total_sales += val
                total_sales_in_period[obj] = total_sales
            else:
                for sale in obj.sales.all():
                    val = sale.sales_value
                    total_sales += val
                total_sales_in_period[obj] = total_sales
        #print(total_sales_in_period, 'total_sales_in_period')

        #for obj in list_of_abc_bjects:                                         ############### ЗАГЛУШКА
        #    total_sales = 0                                                    ############### ЗАГЛУШКА
        #    for sale in obj.sales.all():                                       ############### ЗАГЛУШКА
        #        val = sale.sales_value                                         ############### ЗАГЛУШКА
        #        total_sales += val                                             ############### ЗАГЛУШКА
        #    total_sales_in_period[obj] = total_sales                           ############### ЗАГЛУШКА
        
        # 1.1 объем родаж всех шин за период (ДОРАБОТАТЬ ПО ПЕРИОДАМ)                                                                                    
        list_of_abc_bjects                         
        tyre_total_price = sum(total_sales_in_period.values())

        # 2   ДЛЯ ОТРИСОВКИ ПЕРИОДОВ ПРОДАЖ В ТАБЛИЦЕ (КОЛИЧЕСТВО - клчючи в словаре):

        #period = pandas.date_range("2020-01-01", "2022-09-1", freq='MS')               ################################################# ЗАГЛУШКА -  ПЕРИОД
        if sales_period_for_table:
            sales_period_for_table = list(sales_period_for_table)
            per1 = datetime.strptime(sales_period_for_table[0], '%Y-%m-%d') 
            per2 = datetime.strptime(sales_period_for_table[-1], '%Y-%m-%d') 
            period = pandas.date_range(per1, per2 + pandas.offsets.MonthEnd(), freq='M')                    ####### ВОЗМОЖНЫЙ СБОЙ РАСЧЕТОВ М.Б. ВСЛЕДСТВИИ ОТСЕЧЕК МЕСЯЦЕВ (ПЕРИОДОВ)
        else:
            d = obj.sales.dates('date_of_sales', 'day')
            d = list(d)
            period = pandas.date_range(d[0], d[-1] + pandas.offsets.MonthEnd(), freq='M')                                                    ###### ЗДЕСЬ ЗАДАЕТСЯ ЧАСТОТНОСТЬ ПОИСКА: ДЕНЬ/ МЕСЯЦ/ГОД
        #period = pandas.date_range(sales_period_for_table, freq='MS') 

        list_of_periods = []
        for p in period:                                                                            ######## ОПТИМИЗИРОВАТЬ
            i =  p.year, p.month
            list_of_periods.append(i)
        #print(list_of_periods, 'list_of_periods')

        list_sales_on_period = []
        for obj in list_of_abc_bjects:                                                                ######## ОПТИМИЗИРОВАТЬ
            for period_data in list_of_periods:
                year, month = period_data
                #print(year, month, obj)
                for sale_obj in obj.sales.all().filter(date_of_sales__year=year, date_of_sales__month=month):
                    #print(sale_obj, year, month)
                    params = sale_obj, year, month
                    list_sales_on_period.append(params)
        #print(list_sales_on_period)
        
        lost_keys = []
        for n in list_sales_on_period:                                                              ######## ОПТИМИЗИРОВАТЬ
            yaer = n[1]
            month = n[2]
            zv = yaer, month
            lost_keys.append(zv)
        #print(set(lost_keys))
        unique_keys = set(lost_keys)
        #print(unique_keys, 'unique_keys')

        ##2.1 # продажи шины в конкретный период:            # ключ объект Abcxyz и дата продажи. значение - объекты Sales. ДЛЯ ОТРИСОВКИ ПРОДАЖ ПО МАЛЫМ ПЕРИОДАМ ПО КОНКРЕТНОЙ ШИНЕ 
        for ob in list_of_abc_bjects:
            sale_in_period_list = []
            for period in unique_keys:  
                year, month = period[0], period[1]
                if ob.sales.all().filter(date_of_sales__year=year, date_of_sales__month=month):
                    value = 0
                    for val in ob.sales.all():
                        #print(val.sales_value, 'JHFHHFHFHHF')
                        value += val.sales_value
                        sal_per = value, period
                        #print(sal_per, 'LLLLLL')
                sale_in_period_list.append(sal_per)
        #print(sale_in_period_list)

        #3.1  # Доля в общем объеме, %  
        for obj in total_sales_in_period:
            obj_tyre_total = total_sales_in_period.get(obj)
            if obj_tyre_total == 0:
                #print('ERROR')
                pecent = 0.01
            else:
                pecent = obj_tyre_total/tyre_total_price 
                tyre_percent_in_total_amount[obj] = pecent
        
        # 4.1 сортировка sales по числам  и формирование финального словаря ключ = число год месяц , значения = объекты sales
        list_of_obj_big = []
        for k in unique_keys:                                                                       ######## ОПТИМИЗИРОВАТЬ
            unique_year = k[0]
            unique_month = k[1]
            list_of_obj_small = []
            for obj in list_sales_on_period:
                year = obj[1]
                month = obj[2]
                if year == unique_year and month == unique_month:
                    list_of_obj_small.append(obj[0])
            #dict_list_sales_on_period_final[unique_year, unique_month] = list_of_obj_small 
            dict_list_sales_on_period_final[k] = list_of_obj_small                              ##### СЛОВАРЬ ПЕРИОД ПРОДАЖ  : SALES objects      
        #print(dict_list_sales_on_period_final)    

        # 4.2              # отсортированный список значений продаж шин за период от наибольшего объема к наименьшему + вычисление позиции шины в перечне
        list_of_sale_values = []
        for obj in list_of_abc_bjects: 
            val = total_sales_in_period.get(obj)
            k = val, obj.id, tyre_percent_in_total_amount.get(obj)
            list_of_sale_values.append(k) # id объекта Abcxyz, его значение объем продаж
        list_of_sale_values.sort()
        list_of_sale_values.reverse()
        if len(list_of_sale_values) > 0:
            list_of_sale_values_exist = list_of_sale_values
        ## формирование словарика ключ - шина, значение - позиция в перечне от большего значения объема продаж к меньшему:
        sorted_tyres_list = []              # тип словарик, но это список
        for index_value_per in list_of_sale_values_exist:
            index, value, percent_in_total_amount = index_value_per
            position_in_list_index= len(sorted_tyres_list)
            k = position_in_list_index, index, value, percent_in_total_amount
            sorted_tyres_list.append(k)
        sorted_tyres_dict = {}
        for n in sorted_tyres_list:
            percent_in_total_amount = n[3] 
            obj_index = n[2]
            value = n[1]
            list_position = n[0]
            sorted_tyres_dict[obj_index] = list_position, value, percent_in_total_amount
        #print(sorted_tyres_dict)
        #  формирование процента шины с нарастающим итогом:
        
        accumulated_precent = 0
        for pos in sorted_tyres_dict:
            key_values = pos, sorted_tyres_dict.get(pos)
            #print(key_values, key_values[1][0])
            list_position = key_values[1][0]
            value = key_values[1][1]
            percent_in_total_amount = key_values[1][2]

            kvalues = sorted_tyres_dict.get(pos)
            accumulated_precent += kvalues[2]
            
            accumulated_percent = accumulated_precent  # заглушка
            sorted_tyres_dict_final[key_values[0]] = list_position, value, percent_in_total_amount, accumulated_percent
            
        #print(sorted_tyres_dict_final)          # словарь ключ - pk объекта, значения - позиция в очереди, значение (объем продаж), доля в общем объеме, доля в общем объеме с накопмительным итогом

        # 5.1  продажи шины по периодам:                                                # период - всего шин всех продано
        sales_in_period = 0
        periods_and_sales = dict_list_sales_on_period_final
        period_dict = {}
        for key, value in periods_and_sales.items():                                    ######## ОПТИМИЗИРОВАТЬ
            valuse_list = []
            for obj in list_of_abc_bjects:
                for sale in obj.sales.all():
                    if sale in value:
                        valuse_list.append(sale)

            period_dict[key] = valuse_list
        for key, value in period_dict.items():                                          ######## ОПТИМИЗИРОВАТЬ
            sales_in_period = 0    
            for v in value:
                sales_in_period += v.sales_value
            period_dict_final[key] = sales_in_period
        #print(period_dict_final.values(), 'JJJ')
        #print(period_dict_final, 'GGG')

        period_dict_final = collections.OrderedDict(sorted(period_dict_final.items()))          ## дополнительная сортировка словара дата-значение по датам 
        

        #### 5.2 разбираем продажи шин по периодам:
        ####print(dict_list_sales_on_period_final)
        ###for obj in list_of_abc_bjects:
        ###    for period in dict_list_sales_on_period_final:

        # 6 средне - периодная выручка
        num_periods = len(period_dict_final.keys())
        for obj in list_of_abc_bjects:
            if obj.pk in sorted_tyres_dict_final.keys():
                average_revenue[obj] = sorted_tyres_dict_final.get(obj.pk)[1] / num_periods

        # 7.1 стандартное отклонение standard_deviation
        # получаем продажи шины за период:
        standard_deviation = {}

        tyres_sales_in_period = {}
        for obj in list_of_abc_bjects:
            tyre_total_sales_list = []
            for sale in obj.sales.all():
                val = sale.sales_value
                tyre_total_sales_list.append(val)
            tyres_sales_in_period[obj] = tyre_total_sales_list
        ###############################
            tyre_values_in_period = tyres_sales_in_period.get(obj)
            tyre_average_revenue = average_revenue.get(obj)
            num_periods 
            #if num_periods == 1:
            #    sq_sum = 0
            #    for value in tyre_values_in_period:
            #        sq_sum += (value - tyre_average_revenue) * (value - tyre_average_revenue) 
            #        std_deviation = (sq_sum/(num_periods)) ** (0.5)
            #    #return  "1 заглушка"
            #sq_sum = 0
            #for value in tyre_values_in_period:
            #    sq_sum += (value - tyre_average_revenue) * (value - tyre_average_revenue) 
            #std_deviation = (sq_sum/(num_periods - 1)) ** (0.5)

            sq_sum = 0
            if num_periods == 1:
                sq_sum = 0
                for value in tyre_values_in_period:
                    sq_sum += (value - tyre_average_revenue) * (value - tyre_average_revenue) 
                std_deviation = (sq_sum/(num_periods)) ** (0.5)
            else:
                sq_sum = 0
                for value in tyre_values_in_period:
                    sq_sum += (value - tyre_average_revenue) * (value - tyre_average_revenue) 
                std_deviation = (sq_sum/(num_periods - 1)) ** (0.5)
            standard_deviation[obj] = std_deviation

        # 7.2     Коэффициент вариации:
        variation_coefficien = {}

        for obj in list_of_abc_bjects:
            std_dev = standard_deviation.get(obj)
            av_rev = average_revenue.get(obj)
            variation_coefficient =  std_dev / av_rev
            variation_coefficien[obj] = variation_coefficient

        # 7.3 xyz_group:
        xyz_group_dict = {}
        for obj in list_of_abc_bjects:
            variation_coeff  = variation_coefficien.get(obj)
            if variation_coeff <= 10:
                xyz_group = 'X'
            elif variation_coeff <= 25:
                xyz_group = 'Y'
            elif variation_coeff >= 25:
                xyz_group = 'Z'
            xyz_group_dict[obj] = xyz_group

        # 7.4 abc_xyz_gr
        abc_xyz_group_dict = {}

        for obj in list_of_abc_bjects:
            abc_xyz_group = ''
            if obj.pk in sorted_tyres_dict_final.keys():
                accumulated_percent_value = sorted_tyres_dict_final.get(obj.pk)[3]
                abc_group = ''
                if accumulated_percent_value <= 0.70:
                    abc_group = 'A'
                elif accumulated_percent_value > 0.70 and accumulated_percent_value <= 0.90:
                    abc_group = 'B'
                else:
                    abc_group = 'C'
            xyz_group = xyz_group_dict.get(obj)
            abc_xyz_group = abc_group + xyz_group
            abc_xyz_group_dict[obj] = abc_xyz_group

        # 8 Финальный блок - собираем объекты из Models перед отрисовкой:
        models.TOTAL_SALES_IN_PERIOD = total_sales_in_period
        models.PERCENT_IN_TOTAL_AMOUNT_IN_PERIOD = tyre_percent_in_total_amount
        models.SORTED_WITH_PERCENTS = sorted_tyres_dict_final
        models.AVERAGE_REVENUE = average_revenue
        models.XYZ_GROUP = xyz_group_dict
        models.ABC_XYZ_GROUP = abc_xyz_group_dict
        models.TOTAL_PERIOD_SALES = period_dict_final
        models.TYRE_SALES_IN_SMALL_PERIOD = unique_keys
 
        [[obj.total_sales_in_period(), obj.tyre_percent_in_total_amount_in_period(), obj.percent_in_total_amount_accumulated_percentage(), 
        obj.abc_group(), obj.average_revenue(), obj.xyz_group(), obj.abc_xyz_group()] for obj in list_of_abc_bjects]    

        # 9 Дополнительный блок - подготовка данных для вывода в сводной таблице HOMEPAGE:
        return abc_table

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        #.objects.order_by
        obj = context.get('object')

        # 2  группа шин:
        tyre_groups = dictionaries_models.TyreGroupModel.objects.all()
        tyre_groups_list = []
        for group_name in tyre_groups:
            tyre_groups_list.append(group_name.tyre_group)
        context['tyre_groups'] = tyre_groups_list

        ## 3 типоразмер:
        tyre_sizes = dictionaries_models.TyreSizeModel.objects.all()
        tyre_sizes_list = []
        for tyre_sizes_name in tyre_sizes:
            tyre_sizes_list.append(tyre_sizes_name.tyre_size)
        context['tyre_sizes'] = tyre_sizes_list

        ## 4 модель:
        tire_models = dictionaries_models.ModelNameModel.objects.all()
        tyre_models_list = []
        for tyre_model_name in tire_models:
            tyre_models_list.append(tyre_model_name.model)
        context['tyre_models'] = tyre_models_list

        # подготовка списка объектов отсортированных по значению объем продаж в период:
        list_of_tableobects_dict = {}
        for obj_tyre in obj.table.all():
            if obj_tyre.pk in models.SORTED_WITH_PERCENTS.keys():
                order_numb = models.SORTED_WITH_PERCENTS.get(obj_tyre.pk)[0]
                list_of_tableobects_dict[order_numb] = obj_tyre 
        list_of_tableobects_prepared = []
        for v_tyre in list_of_tableobects_dict.values():
            list_of_tableobects_prepared.append(v_tyre)
        list_of_tableobects_prepared.reverse()
        #print(list_of_tableobects)

        #list_of_tableobects = [tyr_sales for tyr_sales in obj.table.all()]
        #context['list_of_tableobects'] = list_of_tableobects
        context['list_of_tableobects'] = list_of_tableobects_prepared

        # ПОДМЕШИВАЕМ TYRE_CARD для ссылки в template:
        tyr__qset = context.get('list_of_tableobects')
        tyr_card_qset = tyre_models.TyreCard.objects.all()
        list_of_tyr_sal_and_tyr_cards = []
        for tyr_ob in tyr__qset:
            tyr_card_matched = tyr_card_qset.filter(tyre=tyr_ob.tyre)
            if tyr_card_matched:
                tyr_card_matched = tyr_card_qset.get(tyre=tyr_ob.tyre)
                tyr_card_matched = tyr_card_matched.id
            else:
                tyr_card_matched = None
            tyr_sal_and_tyr_cards = tyr_ob, tyr_card_matched
            list_of_tyr_sal_and_tyr_cards.append(tyr_sal_and_tyr_cards)
        context['list_of_tableobects'] = list_of_tyr_sal_and_tyr_cards
        #print(context.get('object_list'))

        return context

class ABCXYZTemplateUpdateView(View):
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


        return HttpResponseRedirect(reverse_lazy('abc_table_xyz:abctable'))