from email.policy import default
from django.db import models
from tyres import models as tyres_model
from sales import models as sales_models

### работа с датами:
import calendar
from datetime import datetime, timedelta
from dateutil import relativedelta

import pandas

###



        ####for obj in self.table.all():
        ####    for obj in obj.sales.all().filter(date_of_sales__range=["2020-01-01", "2022-08-25"]):                    #######  !@!!!!!   РЕШЕНИЕ ВЛОЖЕННЫХ СПИСКОВ для ускорения работы
        ####        print(obj)
                


class AbcxyzTable(models.Model):

    @property
    def tyre_total(self):                                           # объем родаж всех шин за период (ДОРАБОТАТЬ ПО ПЕРИОДАМ)
        tyre_total_price = 0                                                   
        abcxyz_all = self.table.all()                         
        for sale in abcxyz_all:                                                                             ######## ОПТИМИЗИРОВАТЬ
            tyre_total_price += sale.total_sales_of_of_tyre_in_period()    
        return tyre_total_price

    #def table_total_price(self):        
    #    total_tavle_value = 0
    #    for abc_obj in self:
    #        total_tavle_value += abc_obj.total_sales_of_of_tyre_in_period()
    #    
    #    return total_tavle_value             

    def time_delta_calc(self):                              #############################  ДЛЯ ОТРИСОВКИ ПЕРИОДОВ ПРОДАЖ В ТАБЛИЦЕ (КОЛИЧЕСТВО - клчючи в словаре)
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
        for obj in self.table.all():                                                                ######## ОПТИМИЗИРОВАТЬ
            for period_data in list_of_periods:
                year, month = period_data
                #print(year, month, obj)
                for sale_obj in obj.sales.all().filter(date_of_sales__year=year, date_of_sales__month=month):
                    #print(sale_obj, year, month)
                    params = sale_obj, year, month
                    list_sales_on_period.append(params)
        
        lost_keys = []
        for n in list_sales_on_period:                                                              ######## ОПТИМИЗИРОВАТЬ
            yaer = n[1]
            month = n[2]
            zov = yaer, month
            lost_keys.append(zov)
        #print(set(lost_keys))
        unique_keys = set(lost_keys)
        #print('unique_keys = ', unique_keys)

        # сортировка sales по числам  и формирование финального словаря ключ = число год месяц , значения = объекты sales
        dict_list_sales_on_period_final = {}
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
            dict_list_sales_on_period_final[k] = list_of_obj_small 

        #r = relativedelta.relativedelta(date1, date2)           # посмотреть количество дней месяцев и тд
        #def recurs_list_sales_on_period(list_sales):
        #    list_sales
        #    return recurs_list_sales_on_period(list_sales)

        return dict_list_sales_on_period_final              ##### СЛОВАРЬ ПЕРИОД ПРОДАЖ  : SALES objects

    


    def list_of_total_sales_of_of_tyre_in_period(self):              # отсортированный список значений продаж шин за период от наибольшего объема к наименьшему + вычисление позиции шины в перечне
        list_of_sale_values = []
        for obj in self.table.all(): 
            val = obj.total_sales_of_of_tyre_in_period()
            k = val, obj.id, obj.percent_in_total_amount
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
        sorted_tyres_dict_final = {}
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
            
        return sorted_tyres_dict_final          # словарь ключ - pk объекта, значения - позиция в очереди, значение (объем продаж), доля в общем объеме, доля в общем объеме с накопмительным итогом



class Abcxyz(models.Model):
    table = models.ForeignKey(
        AbcxyzTable,
        verbose_name='Таблица',
        related_name='table',                    
        on_delete=models.CASCADE,  
        null=True                       # Заглушка
    ) 
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tyre_abc',
        on_delete=models.PROTECT,
    )
    sales = models.ManyToManyField(
        sales_models.Sales,
        verbose_name='продажи',
        related_name='sales_data',                    
        blank=True,
    )


    def total_sales_of_of_tyre_in_period(self):         # расчет объемов продаж шины за период всего
        total_sales = 0 
        for sale in self.sales.all():
            val = sale.sales_value
            total_sales += val

        #list_obj = []     
        #for sale in self.sales.all().filter(date_of_sales__range=["2019-01-01", "2022-08-25"]):                    #######
        #    total_sales += sale.sales_value

        return total_sales

    @property
    def sales_in_period(self):          # продажи шины по периодам
        sales_in_period = 0
        periods_and_sales = self.table.time_delta_calc()
        period_dict = {}
        for key, value in periods_and_sales.items():                                    ######## ОПТИМИЗИРОВАТЬ
            valuse_list = []
            for sale in self.sales.all():
                if sale in value:
                    valuse_list.append(sale)

            period_dict[key] = valuse_list

        period_dict_final = {}
        for key, value in period_dict.items():                                          ######## ОПТИМИЗИРОВАТЬ
            sales_in_period = 0    
            for v in value:
                sales_in_period += v.sales_value
            period_dict_final[key] = sales_in_period

        return period_dict_final.values                                #### ИТОГОВЫЙ СЛОВАРЬ для формирования (отрисовки) в таблице: ПЕРИОД - ОБЩИЙ ОБЪЕМ ПРОДАЖ ЗА ДАННЫЙ ПЕРИОД для конкретной шины


    @property
    def percent_in_total_amount(self):                  # Доля в общем объеме, %
        if self.table.tyre_total == 0:
            #print('ERROR')
            pecent = 0.1
        else:
            pecent = self.total_sales_of_of_tyre_in_period()/self.table.tyre_total 
        #print(self.total_sales_of_of_tyre_in_period(), self.table.tyre_total, 'percent =', pecent)

        return pecent

    def percent_in_total_amount_percentage(self):                       # %%%%%%%%%%%%%%
        total_sales_percentage = self.percent_in_total_amount * 100
        total_sales_percentage =  float('{:.2f}'.format(total_sales_percentage)) 
        return total_sales_percentage

    def percent_in_total_amount_accumulated(self):       # Доля в общем объеме с накопмительным итогом, %       !
        dict_of_positions = self.table.list_of_total_sales_of_of_tyre_in_period()
        tyre_object = self.id
        dict_key = dict_of_positions.get(tyre_object)
        accumulated_percent = dict_key[3] 
        return accumulated_percent

    def percent_in_total_amount_accumulated_percentage(self):           # %%%%%%%%%%%%%%
        total_sales_percentage = self.percent_in_total_amount_accumulated()  * 100
        total_sales_percentage =  float('{:.2f}'.format(total_sales_percentage)) 
        return total_sales_percentage

    @property
    def abc_group(self):        # принадлежность к группе a b c.   По сути слегка дополняет percent_in_total_amount_accumulated. Можно объединить и возвращать 2 значения и вызов как @property
        accumulated_percent_value = self.percent_in_total_amount_accumulated()
        abc_group = ''
        if accumulated_percent_value <= 0.70:
            abc_group = 'A'
        elif accumulated_percent_value > 0.70 and accumulated_percent_value <= 0.90:
            abc_group = 'B'
        else:
            abc_group = 'C'
        return abc_group

    def average_revenue(self):  #средне - периодная выручка
        num_periods = len(self.table.time_delta_calc())
        average_revenue = self.total_sales_of_of_tyre_in_period()/num_periods
        return average_revenue


    def standard_deviation(self):       #стандартное отклонение
        values_in_period = self.sales_in_period()
        average_revenue = self.average_revenue()
        #print('average_revenue', average_revenue)
        num_periods = len(self.table.time_delta_calc())
        #print('num_periods', num_periods)
        if num_periods == 1:
            sq_sum = 0
            for value in values_in_period:
                sq_sum += (value - average_revenue) * (value - average_revenue) 
                std_deviation = (sq_sum/(num_periods)) ** (0.5)
                return std_deviation
            #return  "1 заглушка"
        sq_sum = 0
        for value in values_in_period:
            sq_sum += (value - average_revenue) * (value - average_revenue) 
        std_deviation = (sq_sum/(num_periods - 1)) ** (0.5)
        return std_deviation
        #return 2342



    def variation_coefficient(self):
        variation_coefficien = 0
        variation_coefficien = self.standard_deviation() / self.average_revenue()
        return variation_coefficien

    def xyz_group(self):
        variation_coefficien  = self.variation_coefficient()
        if variation_coefficien <= 10:
            xyz_group = 'X'
        elif variation_coefficien <= 25:
            xyz_group = 'Y'
        elif variation_coefficien >= 25:
            xyz_group = 'Z'
        return xyz_group

    def abc_xyz_gr(self):



        abc_xyz_group = ''
        abc_group = self.abc_group
        print(abc_group, 'Group aa')
        xyz_group = self.xyz_group()
        print(xyz_group, 'Group xx')
        abc_xyz_group = abc_group + xyz_group



        return abc_xyz_group

