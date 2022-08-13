from multiprocessing import context
from django.shortcuts import render
from . import forms
from . import models
from django.views.generic import TemplateView, ArchiveIndexView
from django.urls import reverse_lazy

from tyres import models as tyres_models
import datetime

#class SalesArchiveIndexView(ArchiveIndexView):
#    model = models.Sales
#    #form_class = forms.SalesForm
#    date_field='date_of_sales'
#    template_name = 'sales/sale.html'
#
#    #def __init__(self, **kwargs):  
#    #    tel = self.request.user.profile.tel
#    #    return {'contact_info': username, 'tel':tel}



class SalesTemplateView(TemplateView):
    model = models.Sales
    #form_class = forms.SalesForm
    template_name = 'sales/sales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tyre_objs = tyres_models.Tyre.objects.all()
        for n in tyre_objs:
            models.Sales.objects.update_or_create(tyre=n, date_of_sales=datetime.datetime.now(), contragent='БНХ УКР', sales_value=10)
        context['sales_all'] = models.Sales.objects.all()   
        return context