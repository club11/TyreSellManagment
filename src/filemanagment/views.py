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



class ExcelTemplateView(LoginRequiredMixin, TemplateView):
#class ExcelTemplateView(View):    
    
    template_name = 'filemanagment/excel_import.html'
    #view_is_async = True

    def get(self, request, *args, **kwargs):
        
        set_time_form_a = f"{settings.hour1}:{settings.minute1}"
        set_time_form_b = f"{settings.hour2}:{settings.minute2}"
        return self.render_to_response({'aform': forms.ImportDataForm(prefix='aform_pre'), 'bform': forms.ImportSalesDataForm(prefix='bform_pre'), 
                                        'dform': forms.ImportTimeForm(initial={'time_task_a': set_time_form_a, 'time_task_b': set_time_form_b})})
    

    def post(self, request, *args, **kwargs):


        if self.request.POST.get('form_name') == "aform.prefix":
            import_data_script.read_from_file(self)
        # если "bform.prefix"  - импорт либо дополнительных данных ценах либо импорт таблицы Химкурьер  
        else:
            #val1, val2 = await import_data_script.read_from_file(self)
            val1, val2 = import_data_script.read_from_file(self)
            if val1 != 'Not chem courier import file':
                print('val1, val2', val1, val2)
                #t2 = threading.Thread(target=import_data_script.read_from_chem_courier_copy_file, args=(val1, val2, import_data_script.chem_courier_bulk_write_ib_bd,))
                t2 = threading.Thread(target=import_data_script.rows_in_file_limiter, args=(val1, val2, ))
                t2.setDaemon(True)
                t2.start()       

    #    if self.request.POST.get('form_name') == "aform.prefix":
    #        form_name = self.request.POST.get('form_name')
    #        if form_name == "aform.prefix":
    #            form = forms.ImportDataForm(self.request.POST, self.request.FILES)
    #            if form.is_valid():
    #                #  Saving POST'ed file to storage
    #                file_to_save = self.request.FILES['file_fields']
    #                file_to_save.name = 'aform_CHEM_.xlsx'
    #                path_to_save = os.path.dirname(os.path.abspath('media')) + '/media/'
    #                file_already_exist = False
    #                # ПРОВЕРКА ЕСТЬ ЛИ УЖЕ СОЗДАННЫЙ ФАЙЛ В СИСТЕМЕ - ЕСЛИ НЕТ _ ТО ЗАПИСАТЬ
    #                for f in os.listdir('media'):
    #                    #path_to = os.path.join('media',f)
    #                    #print('f', f)
    #                    if f == file_to_save.name:
    #                        file_already_exist = True
    #                        break
    #                if not file_already_exist:
    #                    fs = FileSystemStorage()
    #                    fs.save(file_to_save.name, file_to_save)
    #                    #print(file_to_save.name, file_to_save, '=======')     
#
    #                #os.path.join(path_to_save, file_to_save.name)         
#
    #    if self.request.POST.get('form_name') == "bform.prefix":            
    #        form_name = self.request.POST.get('form_name')
    #        if form_name == "bform.prefix":
    #            form = forms.ImportDataForm(self.request.POST, self.request.FILES)
    #            if form.is_valid():
    #                #  Saving POST'ed file to storage
    #                file_to_save = self.request.FILES['file_fields']
    #                file_to_save.name = 'bform_CHEM_.xlsx'
    #                #path_to_save = os.path.dirname(os.path.abspath('media'))# + '/media/'   
    #                path_to_save = os.path.dirname(os.path.abspath('media')) 
    #                file_already_exist = False
    #                for f in os.listdir('media'):
    #                    #print('f', f)
    #                    #path_to = os.path.join('media',f)
    #                    if f == file_to_save.name:
    #                        file_already_exist = True
    #                        break
    #                if not file_already_exist:
    #                    fs = FileSystemStorage()
    #                    fs.save(file_to_save.name, file_to_save)
    #                    #print(file_to_save.name, file_to_save, '=======')   


        #установка времени выполнения импорта:
        if self.request.POST.get('form_name') == "dform.prefix":
            gett_time_a = self.request.POST.get('time_task_a')
            gett_time_b = self.request.POST.get('time_task_b')

            dots_position_a = gett_time_a.find(':')
            if dots_position_a:
                hour1_in_str = gett_time_a[0:dots_position_a]
                minute1_in_str = gett_time_a[dots_position_a+1:]
                if hour1_in_str.isdigit() and minute1_in_str.isdigit() and len(hour1_in_str) < 3 and len(minute1_in_str) < 3:
                    settings.hour1 = int(hour1_in_str)
                    settings.minute1 = int(minute1_in_str)
            #print('settings.hour1 =============== ', settings.hour1)
            dots_position_b = gett_time_b.find(':')
            if dots_position_b:
                hour2_in_str = gett_time_b[0:dots_position_b]
                minute2_in_str = gett_time_b[dots_position_b+1:]
                if hour2_in_str.isdigit() and minute2_in_str.isdigit() and len(hour2_in_str) < 3 and len(minute2_in_str) < 3:
                    settings.hour2 = int(hour2_in_str)
                    settings.minute2 = int(minute2_in_str)
            #print('settings.hour2 =============== ', settings.hour2)

        #перезагрузка сервера nginx
        if self.request.POST.get('form_name') == "cform_reload_nginx.prefix": 
            #subprocess.call('docker exec -it natjusha_project-nginx-1 nginx -s reload')
            #subprocess.run(["systemctl", "reload", "nginx"])
            assss = subprocess.run('ls')
            print('assss===', assss)
            ###subprocess.call(['gunicorn', 'proj.wsgi:application'])


            #cmd = 'gunicorn proj.wsgi:application -b 0.0.0.0:8001'
            #args = shlex.split(cmd)
            #print('args======--==', args)
            #p = subprocess.Popen(args)

            #cmd = 'gunicorn --bind 0.0.0.0:8001 --reload proj:proj'
            #args = shlex.split(cmd)
            #print('args======--==', args)
            #p = subprocess.Popen(args)

            #cmd = 'gunicorn --reload proj:proj'
            #args = shlex.split(cmd)
            #print('args======--==', args)
            #p = subprocess.Popen(args)



                 

        form = forms.ImportSalesDataForm()  

        set_time_form_a = f"{settings.hour1}:{settings.minute1}"
        set_time_form_b = f"{settings.hour2}:{settings.minute2}"        
        #print('!!!ОТРИСОВКА СТРАНИЦЫ ВЫЧИСЛЕНИЯ В БЭКЕ ', self, datetime.now())            
        return render(self.request, 'filemanagment/excel_import.html', {'form': form, 
                                        'dform': forms.ImportTimeForm(initial={'time_task_a': set_time_form_a, 'time_task_b': set_time_form_b})})
    


@app.task
def reading_filemanagementfile():

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
   



async def start_read_file_script():
    await import_data_script.read_from_file()
    print('start_read_file_scrip is running')
    return 'start_read_file_script the programm is fullfilled'



if __name__ == "__main__":
    start_read_file_script()

