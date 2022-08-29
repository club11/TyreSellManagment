from datetime import date
from multiprocessing import context
from pickletools import anyobject
from django.shortcuts import render
from . import models
from tyres import models as tyres_models
from sales import models as sales_models
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy

import datetime
from tyres import models as tyre_model




class AbcxyzTemplateDetailView(DetailView):
    model = models.AbcxyzTable
    template_name = 'abc_table_xyz/abc.html'
    #login_url = reverse_lazy('abc_table_xyz:abctable')


    def get_object(self, queryset=None):                
        # get abc_table
        # ВАРИАНТ РАБОТЫ ПО СЕССИИ: !!! get('table_id')   - хз как он и почему ищет и находит именно по 'table_id'
        #table_id = self.request.session.get('table_id')                 #обращаемся к СЕССИИ текущей
        #print(table_id )
        ################
        abc_table = models.AbcxyzTable.objects.all()[0].pk          # возьмем первый сохданный объект AbcxyzTable - он для всех один - его будут видеть все юзеры

        abc_table, created = models.AbcxyzTable.objects.get_or_create(              #распаковка тапла
        #pk=table_id,                                                      # поле по которому производится поиск
        pk=abc_table,  
        defaults={},
        )
        if created:
            self.request.session['table_id'] = abc_table.pk

        #print(abc_table.time_delta_calc(), 'XXXXXXXXXX')
        
        #a = abc_table.table.all()
        #for k in a:
            #print(k.total_sales_of_of_tyre_in_period(), 'YYY', k.percent_in_total_amount, k.percent_in_total_amount_accumulated(), k.abc_group, k.average_revenue())
            #print(k.sales_in_period())
            #pass

        #for abc_ssales in  models.Abcxyz.objects.all():
            #print(abc_ssales, abc_ssales.sales.all())
            #print('SSAALLLEESS', abc_ssales.sales_in_period)
           
        return abc_table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #.objects.order_by
        obj = context.get('object')
        #print(obj.table.all().order_by('percent_in_total_amount'))
        #print(obj.table.all().order_by('total_sales_of_of_tyre_in_period').reverse())
        list_of_tableobects = []
        for tyr_sales in obj.table.all():
            #print(tyr_sales.total_sales_of_of_tyre_in_period())
            tableobect = tyr_sales.total_sales_of_of_tyre_in_period(), tyr_sales
            list_of_tableobects.append(tableobect)
        def takeFirst(elem):
            return elem[0]
        list_of_tableobects.sort(key=takeFirst)    
        sorted_list_context = []
        for n in list_of_tableobects:
            sorted_list_context.append(n[1])
        sorted_list_context.reverse()
        #print(sorted_list_context)
        context['sorted'] = sorted_list_context
        periods_dates_table_names = (obj.time_delta_calc()).keys()
        context['periods'] = periods_dates_table_names
        #sales_in_period sales_in_period = 
        
        return context



#class AbcxyzTemplateView(TemplateView):
#
#    model = models.AbcxyzTable
#    template_name = 'abc_table_xyz/abc.html'
#    #login_url = reverse_lazy('profiles:login')
#            
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        #0) создадим объект таблицы AbcxyzTable для проверки:
#        abc_table_queryset = models.AbcxyzTable.objects.update_or_create()
#        abc_table = abc_table_queryset[0]
#        #print(abc_table)
#        
#        #### соберем объекты ABC из шин и объектов Sales:
#        # 1) возмем все объекты шин:
#        for obj in tyres_models.Tyre.objects.all():
#            tyre_obj = obj
#        # 2) возмем все объекты продаж:
#            sales_obj_set = sales_models.Sales.objects.filter(tyre=tyre_obj)
#            #print(sales__obj_set)       # <QuerySet [<Sales: Sales object (999)>, <Sales: Sales object (1017)>]>
#            #print(list(sales__obj_set))
#        # 3) создадим объекты модели Abcxyz
#            abc_obj = models.Abcxyz.objects.filter(table=abc_table, tyre=tyre_obj)
#            if abc_obj:
#                #print(abc_obj[0].total_sales_of_of_tyre_in_period())
#                pass
#            else:
#                abc_obj_set = models.Abcxyz.objects.create(
#                    table=abc_table,
#                    tyre = tyre_obj,
#                )
#                for sales_obj in sales_obj_set:
#                    abc_obj_set.sales.add(sales_obj)
#
#        #if abc_table:
#        #    #print(abc_table, '==', abc_table.tyre_total, abc_table.list_of_total_sales_of_of_tyre_in_period())
#        #    pass
#        #
#        #for obj in models.Abcxyz.objects.all():
#        #    #print(obj.total_sales_of_of_tyre_in_period(), obj.percent_in_total_amount())
#        #    print(obj.abc_group[0])
#
#        print(abc_table)
#        context['abc_table'] = abc_table
#        return context
        