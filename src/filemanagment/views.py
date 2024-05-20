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

import sqlalchemy
from sqlalchemy import create_engine
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class ExcelTemplateView(LoginRequiredMixin, TemplateView):
#class ExcelTemplateView(View):    
    
    template_name = 'filemanagment/excel_import.html'
    #view_is_async = True


    def get(self, request, *args, **kwargs):
        return self.render_to_response({'aform': forms.ImportDataForm(prefix='aform_pre'), 'bform': forms.ImportSalesDataForm(prefix='bform_pre')})

    
    def post(self, request, *args, **kwargs):

        if self.request.POST.get('form_name') == "aform.prefix":
            import_data_script.read_from_file(self)
        # если "bform.prefix"  - импорт либо дополнительных данных ценах либо импорт таблицы Химкурьер  
        else:
            val1, val2 = import_data_script.read_from_file(self)
            if val1 != 'Not chem courier import file':
                print('val1, val2', val1, val2)


                #try:
                #db_sqlite3 = os.path.abspath("db.sqlite3")
                #print('PATH db_sqlite3', db_sqlite3)
                #e = create_engine(f'sqlite:{db_sqlite3}', pool_recycle=3600)
                #e = create_engine('sqlite:////src/db.sqlite3')
                    
                ###e = create_engine('sqlite:///sqlite3.db', pool_recycle=39600) 
                ###c = e.connect()
                ###print("Connection was CREATED")

                #except:
                #    pass

                #import_data_script.rows_in_file_limiter(val1, val2, import_data_script.chem_courier_bulk_write_ib_bd)

                #t2 = threading.Thread(target=import_data_script.read_from_chem_courier_copy_file, args=(val1, val2, import_data_script.chem_courier_bulk_write_ib_bd,))
                t2 = threading.Thread(target=import_data_script.rows_in_file_limiter, args=(val1, val2, ))
                t2.setDaemon(False)
                t2.start()  


        form = forms.ImportSalesDataForm()  
        print('!!!ОТРИСОВКА СТРАНИЦЫ ВЫЧИСЛЕНИЯ В БЭКЕ ', self, datetime.now())            
        return render(self.request, 'filemanagment/excel_import.html', {'form': form})
    
       

async def start_read_file_script():
    await import_data_script.read_from_file()
    print('start_read_file_scrip is running')
    return 'start_read_file_script the programm is fullfilled'



if __name__ == "__main__":
    start_read_file_script()

