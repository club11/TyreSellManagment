#from asyncio.windows_events import NULL
import datetime
from datetime import timedelta
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
from prices import views as prices_views

from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
from . import import_data_script
from . import import_data_script_savedread

import asyncio 
from proj import settings

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
from django.core.files.storage import FileSystemStorage

import subprocess, shlex

EXECUTE_CLEAN_BD = None


#from datetime import timedelta
#@app.task()
#def hello():
#    print('Task=======')
#    return 'hello world'
##dt = datetime.now()
##newdatetime = dt.replace(hour=0, minute=59)
##set_time = newdatetime + timedelta(seconds=60)
##set_time = newdatetime
#dt = datetime.now() + timedelta(seconds=120)
#hello.apply_async(eta=dt)


#@app.task
def reading_filemanagementfile():
    print('KUKUKU2221111')
    a_file_name = 'aform_CHEM_.xlsx'
    b_file_name = 'bform_CHEM_.xlsx'
    temporary_created_file_a = False
    print('KUKUKU')
    for f in os.listdir('media'):
        path_to = os.path.join('media',f)
        print('LLLLLL', f, '===', path_to)
        if f == a_file_name:
            temporary_created_file_a = True
            print('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
            break
    temporary_created_file_b = False
    for f in os.listdir('media'):
        print('TTTTTTT', f)
        if f == b_file_name:
            temporary_created_file_b = True
            print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
            break
    #  Reading file from storage
    if temporary_created_file_a is True or temporary_created_file_b is True:
    #1) check files from A_Form or/and check files from B_Form
        import_data_script_savedread.read_from_file()
    #удаление временно созданных файлов воизбежание дубликатов / захламления / шибок
    try:  
        for f in os.listdir('media'):
            path_to = os.path.join('media',f)
            if f == a_file_name:
                os.remove(path_to) 
                print('временный файл aform_CHEM_.xlsx удален')
    except:
        pass
    try:    
        for f in os.listdir('media'):
            path_to = os.path.join('media',f)
            if f == b_file_name:
                os.remove(path_to) 
                print('временный файл bform_CHEM_.xlsx удален')
    except:
        pass


## очистка базы данных
@app.task
def clean_database():
    #print('filemanagementmodels.EXECUTE_CLEAN_BD =======' , filemanagementmodels.EXECUTE_CLEAN_BD)
    global EXECUTE_CLEAN_BD
    print('filemanagementmodels.EXECUTE_CLEAN_BD =======' , EXECUTE_CLEAN_BD)
    #if filemanagementmodels.EXECUTE_CLEAN_BD == 'execute':
    if EXECUTE_CLEAN_BD == 'execute':
        print('CLEANING BD ON THE WAY')
        prices_models.ChemCurierTyresModel.objects.all().delete() 
        prices_models.ComparativeAnalysisTableModel.objects.all().delete() 
        prices_models.CompetitorSiteModel.objects.all().delete() 
        from abc_table_xyz import models as abc_table_xyz_model
        abc_table_xyz_model.Abcxyz.objects.all().delete()
        abc_table_xyz_model.AbcxyzTable.objects.all().delete()
        from sales import models as sl_model 
        sl_model.Tyre_Sale.objects.all().delete()
        sl_model.Sales.objects.all().delete()
        sl_model.SalesTable.objects.all().delete()
        prices_models.SemiVariableCosstModel.objects.all().delete()
        prices_models.PlannedCosstModel.objects.all().delete()
        prices_models.Belarus902PriceModel.objects.all().delete()
        prices_models.TPSRussiaFCAModel.objects.all().delete()
        prices_models.TPSKazFCAModel.objects.all().delete()
        prices_models.TPSMiddleAsiaFCAModel.objects.all().delete()
        prices_models.CurrentPricesModel.objects.all().delete()
        prices_models.ChemCurierTyresModel.objects.all().delete()
        from tyres import models as tr_models
        tr_models.Tyre.objects.all().delete()
        from dictionaries import models as dictionaries_model 
        dictionaries_model.ContragentsModel.objects.all().delete() 
        dictionaries_model.QantityCountModel.objects.all().delete() 
        dictionaries_model.TyreGroupModel.objects.all().delete() 
        dictionaries_model.TyreParametersModel.objects.all().delete() 
        dictionaries_model.ModelNameModel.objects.all().delete()
        dictionaries_model.TyreSizeModel.objects.all().delete()   
        #filemanagementmodels.EXECUTE_CLEAN_BD = None
        EXECUTE_CLEAN_BD = None
    else:
        pass        
## END очистка базы данных



class ExcelTemplateView(LoginRequiredMixin, TemplateView):
#class ExcelTemplateView(View):    
    
    template_name = 'filemanagment/excel_import.html'
    #view_is_async = True

    def get(self, request, *args, **kwargs):
        
        set_time_form_a = f"{settings.hour1}:{settings.minute1}"
        set_time_form_b = f"{settings.hour2}:{settings.minute2}"
        print('set_time_form_a-ISSSS', set_time_form_a)
        return self.render_to_response({'aform': forms.ImportDataForm(prefix='aform_pre'), 'bform': forms.ImportSalesDataForm(prefix='bform_pre'), 
                                        'dform': forms.ImportTimeForm(initial={'time_task_a': set_time_form_a, 'time_task_b': set_time_form_b})})
    

    def post(self, request, *args, **kwargs):

            # OLD VERSION
    #    if self.request.POST.get('form_name') == "aform.prefix":
    #        import_data_script.read_from_file(self)
    #    # если "bform.prefix"  - импорт либо дополнительных данных ценах либо импорт таблицы Химкурьер  
    #    else:
    #        #val1, val2 = await import_data_script.read_from_file(self)
    #        val1, val2 = import_data_script.read_from_file(self)
    #        if val1 != 'Not chem courier import file':
    #            print('val1, val2', val1, val2)
    #            #t2 = threading.Thread(target=import_data_script.read_from_chem_courier_copy_file, args=(val1, val2, import_data_script.chem_courier_bulk_write_ib_bd,))
    #            t2 = threading.Thread(target=import_data_script.rows_in_file_limiter, args=(val1, val2, ))
    #            t2.setDaemon(True)
    #            t2.start()       
            # END OLD VERSION

        if self.request.POST.get('form_name') == "aform.prefix":
            form_name = self.request.POST.get('form_name')
            if form_name == "aform.prefix":
                form = forms.ImportDataForm(self.request.POST, self.request.FILES)
                if form.is_valid():
                    #  Saving POST'ed file to storage
                    file_to_save = self.request.FILES['file_fields']
                    file_to_save.name = 'aform_CHEM_.xlsx'
                    path_to_save = os.path.dirname(os.path.abspath('media')) + '/media/'
                    file_already_exist = False
                    # ПРОВЕРКА ЕСТЬ ЛИ УЖЕ СОЗДАННЫЙ ФАЙЛ В СИСТЕМЕ - ЕСЛИ НЕТ _ ТО ЗАПИСАТЬ
                    for f in os.listdir('media'):
                        #path_to = os.path.join('media',f)
                        #print('f', f)
                        if f == file_to_save.name:
                            file_already_exist = True
                            break
                    if not file_already_exist:
                        fs = FileSystemStorage()
                        fs.save(file_to_save.name, file_to_save)
                        #print(file_to_save.name, file_to_save, '=======')     

                    #os.path.join(path_to_save, file_to_save.name)         

        if self.request.POST.get('form_name') == "bform.prefix":            
            form_name = self.request.POST.get('form_name')
            if form_name == "bform.prefix":
                form = forms.ImportDataForm(self.request.POST, self.request.FILES)
                if form.is_valid():
                    #  Saving POST'ed file to storage
                    file_to_save = self.request.FILES['file_fields']
                    file_to_save.name = 'bform_CHEM_.xlsx'
                    #path_to_save = os.path.dirname(os.path.abspath('media'))# + '/media/'   
                    path_to_save = os.path.dirname(os.path.abspath('media')) 
                    file_already_exist = False
                    for f in os.listdir('media'):
                        #print('f', f)
                        #path_to = os.path.join('media',f)
                        if f == file_to_save.name:
                            file_already_exist = True
                            break
                    if not file_already_exist:
                        fs = FileSystemStorage()
                        fs.save(file_to_save.name, file_to_save)
                        #print(file_to_save.name, file_to_save, '=======')   


        #установка времени выполнения импорта:
        if self.request.POST.get('form_name') == "dform.prefix":
            gett_time_a = self.request.POST.get('time_task_a')
            gett_time_b = self.request.POST.get('time_task_b')

            dots_position_a = gett_time_a.find(':')
            if dots_position_a:
                hour1_in_str = gett_time_a[0:dots_position_a]
                minute1_in_str = gett_time_a[dots_position_a+1:]
                if hour1_in_str.isdigit() and minute1_in_str.isdigit() and len(hour1_in_str) < 3 and len(minute1_in_str) < 3:
                    settings.hour1 = int(hour1_in_str)      #чистая косметика
                    settings.minute1 = int(minute1_in_str)  #чистая косметика

                    hour1_in_int = int(hour1_in_str)
                    minute1_in_int = int(minute1_in_str)
                    dt = datetime.now()
                    dt = dt.replace(hour=hour1_in_int, minute=minute1_in_int)
                    dt = dt - timedelta(hours=3)         #сдвиг времени выполлнения по серваку на 3 часа назад
                    #dt = datetime.strptime(f'{hour1_in_int}:{minute1_in_int}', '%H:%M').time()
                    print('DDDDDTTTTT', dt)
                    prices_views.running_programm.apply_async(eta=dt)          ### ВСЯ МАГИЯ ЗДЕСЬ

            #print('settings.hour1 =============== ', settings.hour1)
            dots_position_b = gett_time_b.find(':')
            if dots_position_b:
                hour2_in_str = gett_time_b[0:dots_position_b]
                minute2_in_str = gett_time_b[dots_position_b+1:]
                if hour2_in_str.isdigit() and minute2_in_str.isdigit() and len(hour2_in_str) < 3 and len(minute2_in_str) < 3:
                    settings.hour2 = int(hour2_in_str)      #чистая косметика
                    settings.minute2 = int(minute2_in_str)  #чистая косметика

                    hour2_in_int = int(hour2_in_str)
                    minute2_in_int = int(minute2_in_str)
                    #dt = datetime.strptime(f'{hour2_in_int}:{minute2_in_int}', '%H:%M').time()
                    dt = datetime.now()
                    dt = dt.replace(hour=hour2_in_int, minute=minute2_in_int)
                    dt = dt - timedelta(hours=3)         #сдвиг времени выполлнения по серваку на 3 часа назад
                    reading_filemanagementfile.apply_async(eta=dt)      ### ВСЯ МАГИЯ ЗДЕСЬ

            #print('settings.hour2 =============== ', settings.hour2)

        if self.request.POST.get('form_name') == "cform_reload_nginx.prefix": 
            subprocess.call('docker restart tyresellmanagment-src')       

        from proj import celery

        print('==========IFIFIFIFIFIFIIFI 1==', celery.app.control.inspect())
        i = celery.app.control.inspect()
        print('==========IFIFIFIFIFIFIIFI Show the items that have an ETA or are scheduled for later processing 2==', i.scheduled())
        print('==========IFIFIFIFIFIFIIFI Show tasks that are currently active 3==', i.active())
        print('==========IFIFIFIFIFIFIIFI Show tasks that have been claimed by workers 4==', i.reserved())


    
        form = forms.ImportSalesDataForm()  
        set_time_form_a = f"{settings.hour1}:{settings.minute1}"
        set_time_form_b = f"{settings.hour2}:{settings.minute2}"        
        #print('!!!ОТРИСОВКА СТРАНИЦЫ ВЫЧИСЛЕНИЯ В БЭКЕ ', self, datetime.now())            
        

        # очистить базу данных:
        if self.request.POST.get('form_name') == "delete_data_base_form.prefix":
            print('WE GOT 2 MIN TASK AWAIT')
            execute_in_two_minutes = datetime.now() + timedelta(minutes = 2)
            #filemanagementmodels.EXECUTE_CLEAN_BD = 'execute'
            global EXECUTE_CLEAN_BD
            EXECUTE_CLEAN_BD = 'execute'
            clean_database.apply_async(eta=execute_in_two_minutes)
        # END очистить базу данных:
  
        return render(self.request, 'filemanagment/excel_import.html', {'form': form, 
                                        'dform': forms.ImportTimeForm(initial={'time_task_a': set_time_form_a, 'time_task_b': set_time_form_b})})
    


async def start_read_file_script():
    await import_data_script.read_from_file()
    print('start_read_file_scrip is running')
    return 'start_read_file_script the programm is fullfilled'



if __name__ == "__main__":
    start_read_file_script()

