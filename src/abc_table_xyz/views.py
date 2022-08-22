from datetime import date
from multiprocessing import context
from django.shortcuts import render
from . import models
from tyres import models as tyres_models
from sales import models as sales_models
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy

import datetime
from tyres import models as tyre_model

class AbcxyzTemplateView(TemplateView,):
    model = models.AbcxyzTable
    template_name = 'abc_table_xyz/abc.html'
    #login_url = reverse_lazy('profiles:login')
            
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #0) создадим объект таблицы AbcxyzTable для проверки:
        abc_table_queryset = models.AbcxyzTable.objects.update_or_create()
        abc_table = abc_table_queryset[0]
        #print(abc_table)
        

        #### соберем объекты ABC из шин и объектов Sales:
        # 1) возмем все объекты шин:
        for obj in tyres_models.Tyre.objects.all():
            tyre_obj = obj
        # 2) возмем все объекты продаж:
            sales_obj_set = sales_models.Sales.objects.filter(tyre=tyre_obj)
            #print(sales__obj_set)       # <QuerySet [<Sales: Sales object (999)>, <Sales: Sales object (1017)>]>
            #print(list(sales__obj_set))
        # 3) создадим объекты модели Abcxyz
            abc_obj = models.Abcxyz.objects.filter(table=abc_table, tyre=tyre_obj)
            if abc_obj:
                #print(abc_obj[0].total_sales_of_of_tyre_in_period())
                pass
            else:
                abc_obj_set = models.Abcxyz.objects.create(
                    table=abc_table,
                    tyre = tyre_obj,
                )
                for sales_obj in sales_obj_set:
                    abc_obj_set.sales.add(sales_obj)


        if abc_table:
            #print(abc_table, '==', abc_table.tyre_total, abc_table.list_of_total_sales_of_of_tyre_in_period())
            pass

        for obj in models.Abcxyz.objects.all():
            #print(obj.total_sales_of_of_tyre_in_period(), obj.percent_in_total_amount())
            print(obj.percent_in_total_amount_accumulated())



        return self.render_to_response(context)
#
        ##cart_id = self.request.session.get('cart_id')               #обращаемся к СЕССИИ текущей
        ##table = models.AbcxyzTable.objects.get_or_create(          #распаковка тапла
 