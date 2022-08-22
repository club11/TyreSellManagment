from gc import get_objects
from multiprocessing import context
from django.shortcuts import render
from . import forms
from . import models
from django.views.generic import TemplateView, ArchiveIndexView, ListView
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



class SalesTemplateListView(ListView):

    model = models.Sales
    template_name = 'sales/sales.html'

