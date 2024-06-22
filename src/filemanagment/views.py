#from asyncio.windows_events import NULL
import datetime
from enum import unique
from operator import index
#from turtle import st
from unicodedata import decimal, name
from webbrowser import get
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, View
from . import forms
from . import models as filemanagementmodels
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
from . import import_data_script_savedread

import asyncio 

import threading
from threading import Timer
#import multiprocessing

import sqlalchemy
from sqlalchemy import create_engine
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from celery import shared_task
from proj.celery import app
from django.core.files.storage import default_storage



class ExcelTemplateView(LoginRequiredMixin, TemplateView):
#class ExcelTemplateView(View):    
    
    template_name = 'filemanagment/excel_import.html'
    #view_is_async = True

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'aform': forms.ImportDataForm(prefix='aform_pre'), 'bform': forms.ImportSalesDataForm(prefix='bform_pre')})
    

    def post(self, request, *args, **kwargs):

        #if self.request.POST.get('form_name') == "aform.prefix":
        #    import_data_script.read_from_file(self)
        ## если "bform.prefix"  - импорт либо дополнительных данных ценах либо импорт таблицы Химкурьер  
        #else:
        #    #val1, val2 = await import_data_script.read_from_file(self)
        #    val1, val2 = import_data_script.read_from_file(self)
        #    if val1 != 'Not chem courier import file':
        #        print('val1, val2', val1, val2)
        #        #t2 = threading.Thread(target=import_data_script.read_from_chem_courier_copy_file, args=(val1, val2, import_data_script.chem_courier_bulk_write_ib_bd,))
        #        t2 = threading.Thread(target=import_data_script.rows_in_file_limiter, args=(val1, val2, ))
        #        t2.setDaemon(True)
        #        t2.start()       

        if self.request.POST.get('form_name') == "aform.prefix":
            form_name = self.request.POST.get('form_name')
            if form_name == "aform.prefix":
                form = forms.ImportDataForm(self.request.POST, self.request.FILES)
                if form.is_valid():
                    #  Saving POST'ed file to storage
                    file_to_save = self.request.FILES['file_fields']
                    file_to_save.name = 'aform_CHEM_.xlsx'
                    default_storage.save(file_to_save.name, file_to_save)              
        else:            
            form_name = self.request.POST.get('form_name')
            if form_name == "bform.prefix":
                form = forms.ImportDataForm(self.request.POST, self.request.FILES)
                if form.is_valid():
                    #  Saving POST'ed file to storage
                    file_to_save = self.request.FILES['file_fields']
                    file_to_save.name = 'bform_CHEM_.xlsx'
                    default_storage.save(file_to_save.name, file_to_save)

        form = forms.ImportSalesDataForm()  
        print('!!!ОТРИСОВКА СТРАНИЦЫ ВЫЧИСЛЕНИЯ В БЭКЕ ', self, datetime.now())            
        return render(self.request, 'filemanagment/excel_import.html', {'form': form})
    

@app.task
def reading_filemanagementfile():
    try:
        temporary_created_file_a = os.path.abspath('aform_CHEM_.xlsx')
        temporary_created_file_b = os.path.abspath('bform_CHEM_.xlsx')
    except: 
        pass
    #  Reading file from storage
    if temporary_created_file_a:
    #1) check files from A_Form
        import_data_script_savedread.read_from_file()
    if temporary_created_file_b:
    #2) check files from B_Form
        import_data_script_savedread.read_from_file()
    
    try:  
        temporary_created_file1 = os.path.abspath('aform_CHEM_.xlsx') 
        print('temporary_created_file1', temporary_created_file1)
        os.remove(temporary_created_file1, dir_fd=None)
        print('временный файл aform_CHEM_.xlsx удален')
    except:
        pass
    try:    
        temporary_created_file2 = os.path.abspath('bform_CHEM_.xlsx')  
        print('temporary_created_file2', temporary_created_file2)
        os.remove(temporary_created_file2, dir_fd=None)
        print('временный файл bform_CHEM_.xlsx удален')
    except:
        pass



async def start_read_file_script():
    await import_data_script.read_from_file()
    print('start_read_file_scrip is running')
    return 'start_read_file_script the programm is fullfilled'



if __name__ == "__main__":
    start_read_file_script()

