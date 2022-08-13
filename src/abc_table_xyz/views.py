from datetime import date
from multiprocessing import context
from django.shortcuts import render
from . import models
from django.views.generic import TemplateView
from django.urls import reverse_lazy

import datetime
from tyres import models as tyre_model

class AbcxyzTemplateView(TemplateView):
    model = models.Abcxyz
    template_name = 'abc_table_xyz/main.html'
    #login_url = reverse_lazy('profiles:login')

    #def get_context_data(self, **kwargs):
#
    #    d = datetime.date(1997, 10, 19)
    #    tyre_in_abc = models.Abcxyz()
    #    tyre_in_abc.tyre = tyre_model.Tyre.objects.get(pk=1)
    #    tyre_in_abc.date_of_sales = d
    #    tyre_in_abc.sales_on_date = 2
    #    tyre_in_abc.table = models.AbcxyzTable.objects.all()[0]
    #    tyre_in_abc.save()
    #    
    #    context = super().get_context_data(**kwargs)
    #    context['tyre_in_abc'] = tyre_in_abc
#
    #    return super().get_context_data(**kwargs)