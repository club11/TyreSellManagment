#from asyncio.windows_events import NULL
import datetime
from enum import unique
from operator import index
from turtle import st
from unicodedata import decimal, name
from webbrowser import get
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, View
from . import forms
from . import models
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import openpyxl 
import openpyxl.utils.cell
import re
from dictionaries import models as dictionaries_models
from tyres import models as tyres_models
from sales import models as sales_models
from itertools import count, islice
from abc_table_xyz import models as abc_table_xyz_models
from datetime import datetime
from prices import models as prices_models

from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
from . import import_data_script

import asyncio 

import threading
from threading import Timer
#import multiprocessing




class ExcelTemplateView(TemplateView):
#class ExcelTemplateView(View):    
    
    template_name = 'filemanagment/excel_import.html'
    #view_is_async = True


    def get(self, request, *args, **kwargs):
        return self.render_to_response({'aform': forms.ImportDataForm(prefix='aform_pre'), 'bform': forms.ImportSalesDataForm(prefix='bform_pre')})

    
    def post(self, request, *args, **kwargs):
        #chem_cour_value = import_data_script.read_from_file(self)

        t = threading.Thread(target=import_data_script.chem_courier_bulk_write_ib_bd, args=(chem_cour_value,))
        t.setDaemon(False)
        t.start()

    ###    ###p = multiprocessing.Process(target=import_data_script.read_from_file(self))
    ###    ###p.start()
    ###    #Timer(2, import_data_script.read_from_file(self)).start()
    ###    ####try:
    ###    ####    form = forms.ImportSalesDataForm()  
    ###    ####    return render(self.request, 'filemanagment/excel_import.html', {'form': form})
    ###    ####finally:
    ###    ####    import_data_script.read_from_file(self)


        form = forms.ImportSalesDataForm()  
        print('!!! FORMA ', self, datetime.now())            
        return render(self.request, 'filemanagment/excel_import.html', {'form': form})
    
       

async def start_read_file_script():
    await import_data_script.read_from_file()
    print('start_read_file_scrip is running')
    return 'start_read_file_script the programm is fullfilled'



if __name__ == "__main__":
    start_read_file_script()

