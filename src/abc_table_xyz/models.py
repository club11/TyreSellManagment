from email.policy import default
from django.db import models
from tyres import models as tyres_model
from sales import models as sales_models

class AbcxyzTable(models.Model):

    @property
    def tyre_total(self):                                           # объем родаж всех шин за период (ДОРАБОТАТЬ ПО ПЕРИОДАМ)
        tyre_total_price = 0                                                   
        abcxyz_all = self.table.all()                         
        for sale in abcxyz_all:
            tyre_total_price += sale.total_sales_of_of_tyre_in_period()  
        return tyre_total_price


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
            

        return sorted_tyres_dict_final


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

    def total_sales_of_of_tyre_in_period(self):         # расчет объемов продаж шины за период 
        total_sales = 0 
        for sale in self.sales.all():
            total_sales += sale.sales_value
        return total_sales

    @property
    def percent_in_total_amount(self):                  # Доля в общем объеме, %
        pecent = self.total_sales_of_of_tyre_in_period()/self.table.tyre_total
        #print(self.total_sales_of_of_tyre_in_period(), self.table.tyre_total, 'percent =', pecent)
        return pecent

    def percent_in_total_amount_accumulated(self):       # Доля в общем объеме с накопмительным итогом, %
        dict_of_positions = self.table.list_of_total_sales_of_of_tyre_in_period()
        tyre_object = self.id
        dict_key = dict_of_positions.get(tyre_object)
        accumulated_percent = dict_key[3]
        return accumulated_percent