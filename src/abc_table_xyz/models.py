from email.policy import default
from multiprocessing.resource_sharer import stop
from django.db import models
from tyres import models as tyres_model
from sales import models as sales_models
from django.contrib.auth import get_user_model
User = get_user_model()

TOTAL_SALES_IN_PERIOD = 0
PERCENT_IN_TOTAL_AMOUNT_IN_PERIOD = {}
SORTED_WITH_PERCENTS = {}
AVERAGE_REVENUE = {}
XYZ_GROUP = {}
ABC_XYZ_GROUP = {}
TOTAL_PERIOD_SALES = {}
TYRE_SALES_IN_SMALL_PERIOD = {}

#UPDATE_VIEW:
PERIOD_UPDATE_SALES = ''
TYRE_GROUP_NAMES = []
TYRE_GROUP_SIZES = []
TYRE_GROUP_MODELS = []

def period_counter_generator(list_of_periods):
    for period in list_of_periods:
        yield period

        ####for obj in self.table.all():
        ####    for obj in obj.sales.all().filter(date_of_sales__range=["2020-01-01", "2022-08-25"]):                    #######  !@!!!!!   РЕШЕНИЕ ВЛОЖЕННЫХ СПИСКОВ для ускорения работы
        ####        print(obj)
class AbcxyzTable(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='ABCТаблица',
        related_name='abcxyz_table',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    def period_dict_final(self):
        table_period_headers = TOTAL_PERIOD_SALES.keys()
        #print(table_period_headers)
        return table_period_headers 

    def tyre_sales_sold_in_small_period(self):
        table_period_headers = TOTAL_PERIOD_SALES.keys()
        return table_period_headers

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
    def total_sales_in_period(self):
        for obj_key in TOTAL_SALES_IN_PERIOD:
            if self == obj_key:
                total_sales_in_period = TOTAL_SALES_IN_PERIOD.get(obj_key)
        return total_sales_in_period

    def tyre_percent_in_total_amount_in_period(self):
        for obj_key in PERCENT_IN_TOTAL_AMOUNT_IN_PERIOD:
            if self == obj_key:
                tyre_percent_in_total_amount_in_period = PERCENT_IN_TOTAL_AMOUNT_IN_PERIOD.get(obj_key) * 100
                tyre_percent_in_total_amount_in_period =  float('{:.2f}'.format(tyre_percent_in_total_amount_in_period)) 
        return tyre_percent_in_total_amount_in_period

    def percent_in_total_amount_accumulated_percentage(self):
        for obj_key in SORTED_WITH_PERCENTS:
            if self.pk == obj_key:
                tyre_order_number = SORTED_WITH_PERCENTS.get(obj_key)[3] * 100
                tyre_order_number =  float('{:.2f}'.format(tyre_order_number)) 
        return tyre_order_number
    
    def order_number(self):                                                     # № очередности для выводя объекта в template
        for obj_key in SORTED_WITH_PERCENTS:
            if self.pk == obj_key:
                tyre_order_number = SORTED_WITH_PERCENTS.get(obj_key)[0]
        return tyre_order_number

    def abc_group(self):        # принадлежность к группе a b c.  
        for obj_key in SORTED_WITH_PERCENTS:
            if self.pk == obj_key: 
                accumulated_percent_value = SORTED_WITH_PERCENTS.get(obj_key)[3]
                abc_group = ''
                if accumulated_percent_value <= 0.70:
                    abc_group = 'A'
                elif accumulated_percent_value > 0.70 and accumulated_percent_value <= 0.90:
                    abc_group = 'B'
                else:
                    abc_group = 'C'
        return abc_group

    def average_revenue(self):
        for obj_key in AVERAGE_REVENUE:
            if self == obj_key:
                average_revenue = AVERAGE_REVENUE.get(obj_key)
                average_revenue =  float('{:.2f}'.format(average_revenue)) 
        return average_revenue

    def xyz_group(self):
        for obj_key in XYZ_GROUP:
            if self == obj_key:
                xyz_group = XYZ_GROUP.get(obj_key)
        return xyz_group

    def abc_xyz_group(self):
        for obj_key in ABC_XYZ_GROUP :
            if self == obj_key:
                abc_xyz_group = ABC_XYZ_GROUP.get(obj_key)
        return abc_xyz_group

    def return_val(self):
        tyre_in_period_sale_dict = {}
        periods = TOTAL_PERIOD_SALES.keys()
        for per in periods:
            year = per[0]
            month = per[1]
            sales_in_period = self.sales.all().filter(date_of_sales__year=year, date_of_sales__month=month)
            total_per_value = 0 
            for sal in sales_in_period:
                total_per_value += sal.sales_value
            tyre_in_period_sale_dict[per] = total_per_value
        return tyre_in_period_sale_dict.values()








