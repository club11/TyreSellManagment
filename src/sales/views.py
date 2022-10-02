from gc import get_objects
from multiprocessing import context
from django.shortcuts import render
from . import forms
from . import models
from django.views.generic import ArchiveIndexView, ListView, DetailView
from django.urls import reverse_lazy
from tyres import models as tyres_models
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
        list_of_sale_objects = only_one_exsted_sales_table.sales_table.all()    # 2.    все объекты sales в данной таблице SalesTable
        # 2. получение всех дат:
        list_of_dates = list(list_of_sale_objects.dates('date_of_sales', 'day'))
        models.SALES_DATES = list_of_dates
        #
        
        # 3. FПолучение словаря ШИНА - sales на дату, контрагент
        #for tyre in only_one_exsted_sales_table.table_sales.all():
        #    print(tyre)
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
            for sal in obj.tyre.sales.all():
                tyre_sal_total += sal.sales_value
            tyre_sal_total_dict[obj] = tyre_sal_total
        
        models.TYRE_SAL_TOTAL_DICT = tyre_sal_total_dict
        
        #[[obj.sale_on_date(), obj.contragents(), obj.contragents_sales(), obj.contragents_sales_joined(),] for obj in list_of_tyre_sales] 
        [[obj.sale_on_date(), obj.contragents_sales(), obj.contragents_sales_joined(), obj.total_sale_in_period()] for obj in list_of_tyre_sales] 
        return sales_table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context.get('object')
   
        sal_tyr_objects = obj.table_sales.all()
        list_of_sal_tyres = []
        for object in sal_tyr_objects:
            list_of_sal_tyres.append(object)

        list_of_sal_tyres.reverse()
        context['list_objects'] = list_of_sal_tyres
        return context

