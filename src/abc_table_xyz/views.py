from datetime import date
from multiprocessing import context
from multiprocessing.resource_sharer import stop
from pickletools import anyobject
from pyexpat import model
from django.shortcuts import render
from . import models
from tyres import models as tyres_models
from sales import models as sales_models
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy

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


        # 1 расчет объемов продаж шины за период всего:     (ДОРАБОТАТЬ ПО ПЕРИОДАМ)                                  
        for obj in list_of_abc_bjects:
            total_sales = 0 
            for sale in obj.sales.all():
                val = sale.sales_value
                total_sales += val
            total_sales_in_period[obj] = total_sales
        #print(total_sales_in_period, 'total_sales_in_period')

        # 1.1 объем родаж всех шин за период (ДОРАБОТАТЬ ПО ПЕРИОДАМ)                                                                                    
        list_of_abc_bjects                         
        tyre_total_price = sum(total_sales_in_period.values())

        # 2   ДЛЯ ОТРИСОВКИ ПЕРИОДОВ ПРОДАЖ В ТАБЛИЦЕ (КОЛИЧЕСТВО - клчючи в словаре):
        date1 = datetime.strptime(str('2021-08-15 12:00:00'), '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(str('2022-08-15'), '%Y-%m-%d')
        delta = date2 - date1
        days = [date1 + timedelta(days=i) for i in range(delta.days + 1)]
        #return list(map(lambda n: n.strftime("%Y-%m-%d"), days))

        #period = date2 - date1
        period = pandas.date_range("2020-01-01", "2022-08-25", freq='MS')
        #print(period)

        list_of_periods = []
        for p in period:                                                                            ######## ОПТИМИЗИРОВАТЬ
            i =  p.year, p.month
            list_of_periods.append(i)
        #print(list_of_periods)

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
            zov = yaer, month
            lost_keys.append(zov)
        #print(set(lost_keys))
        unique_keys = set(lost_keys)
        #print(unique_keys, 'unique_keys')

        ##2.1 # продажи шины в конкретный период:            # ключ объект Abcxyz и дата продажи. значение - объекты Sales. ДЛЯ ОТРИСОВКИ ПРОДАЖ ПО МАЛЫМ ПЕРИОДАМ ПО КОНКРЕТНОЙ ШИНЕ 

        ####
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
        #print(period_dict_final.values())
        #print(period_dict_final)

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

        #def takeFirst(elem):
        #    return elem[0]
        #list_of_tableobects.sort(key=takeFirst)    

        #sorted_list_context = [n[1] for n in list_of_tableobects] #sorted_list_context = [] #for n in list_of_tableobects: #    sorted_list_context.append(n[1])
        return context