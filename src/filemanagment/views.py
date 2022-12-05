from asyncio.windows_events import NULL
import datetime
from enum import unique
from operator import index
from turtle import st
from unicodedata import decimal, name
from webbrowser import get
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from . import forms
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

class ExcelTemplateView(TemplateView):
    template_name = 'filemanagment/excel_import.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'aform': forms.ImportDataForm(prefix='aform_pre'), 'bform': forms.ImportSalesDataForm(prefix='bform_pre')})

    def post(self, request, *args, **kwargs):
        form_name = self.request.POST.get('form_name')
        row_value = int
        tyresize_list = []
        tyremodel_list = []
        tyreparametrs_list = [] 
        sales_list = []                 #объем продаж на дату
        planned_costs = []              #плановая себестоимость/плановые затраты planned_costs 
        semi_variable_costs = []        #плановая себестоимость
        belarus902price_costs = []      #прейскуранты №№9, 902
        tpsrussiafcaprice_costs = []    #ТПС РФ FCA
        tpskazfcaprice_costs = []       #ТПС Казахстан FCA
        tpsmiddleasiafcaprice_costs = [] #ТПС Азия
        current_prices = []   # Действующие цены
        contragent_list = []            #контрагент
        column_sell_date = ''           #строка с датой продажи
        tyretype_row_dict = {}          # словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = типоразмер
        model_row_dict = {}             # словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = модель
        params_row_dict = {}            # словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = параметры
        saless_row_dict = {}            # словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = объем продаж
        planned_costs_row_dict = {}     # словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = плановая себестоимость
        semi_variable_costs_row_dict = {} # словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = прямые затраты
        belarus902price_costs_row_dict = {}# словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = прейскуранты №№9, 902
        tpsrussiafcaprice_costs_row = {}# словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = ТПС РФ FCA
        tpskazfcaprice_cost_row = {}# словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = ТПС Казахстан FCA
        tpsmiddleasiafcaprice_costs_row = {}# словарь, в который закидываются данные из строк построчно. ключ - номер строки, параметры  = ТПС Средняя Азия, Закавказье, Молдова FCA
        current_prices_row = {}                 # словарь, в который закидываются данные о действующих ценах

        row_parsing_sales_costs_prices_dict = {}     # словарь, в который закидываются данные из строк построчно. ключ - шина, параметры = данные о продажах, минималках и прайсах


        #date_period =   #ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ ДЛДЯ СЕБЕСТОИМОСТИ и прайсов
        ply_dict = {}
        load_speed_index_dict = {}
        dict_of_param_to_remake_in_standart = {
                ('Сер', 'Ср'):'сер',
                ('Груз', 'Гр'):'груз',
                ('Легк', 'Лег', 'Лг'):'легк',
                ('Сх', 'С/х'):'сх',
                ('Л/г', 'л/г'):'л/г',
                ('Тр', 'Тп', 'Трп'):'трп',
                'L-2':'L-2',
                'LS-2':'LS-2',
                ('Type', 'Typ'):'Type',
                'кам':'кам',
                ('б/к', 'бк'):'б/к',
                ('ошип', 'ош', 'п/ош'):'ошип',
                'КГШ':'КГШ',
                'ЗМШ':'ЗМШ',
                'ВАЗ':'ВАЗ',
                'а/к':'а/к',
                'о/л':'о/л',
                'ак23.5':'ак23.5',
                'ол23.5':'ол23.5',
                'Газель':'Газель',
                'Вездеход':'Вездеход',
                'погр':'Погр',
                'масс':'Масс',
                ('выт', 'камневыт.'):'камневыт',
                'вен.161':'вен.161',
                'вен.ТК':'вен.ТК',
                'H':'H',
                'S':'S',
                'C':'C',
                #'РК-\d{1}-\d{3}',
                #'РК-\d{1}([А-Яа-я]|[A-Za-z])-\d{3}',
                #'ГК--\d{3}',
                #' (\d{2}|\d{1})\b',
                #'\d{3}([А-Яа-я]|[A-Za-z])\d{1}|\d{3} ([А-Яа-я]|[A-Za-z])\d{1}',
            }
        if form_name == "aform.prefix":
            form = forms.ImportDataForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                file_to_read = openpyxl.load_workbook(self.request.FILES['file_fields'], data_only=True)     
                sheet = file_to_read['Sheet1']      # Читаем файл и лист1 книги excel
                #print(f'Total Rows = {sheet.max_row} and Total Columns = {sheet.max_column}')               # получить количество строк и колонок на листе
                # 1. Парсинг. поиск ячейки с названием 'Наименование продукции' и выборка данных из данной колонки с заголовком этой ячейки            
                for row in sheet.rows:                      
                    for cell in row:
                        if cell.value == 'Наименование продукции':
                            for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):   
                                ### проверка если строка пустая
                                if str(row[cell.column-1].value) is not str(row[cell.column-1].value):        
                                    tyresize_list.append(' ')
                                #######
                                reg_list = [
                                #'\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2})', 
                                #'\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2}', 
                                #'(\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2})',  # = '(\d{3}|\d{2})/\d{2}([A-Za-z]|-)\d{2}' +  '\d{3}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',    
                                '(\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}))|(\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2})|((\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2}))', #3 в одном чтобы избежать повторений двойных в ячейке наподобие #АШ 480/80R42(18.4R42)
                                '\d{2}(\.|\,)\d{1}[A-Za-z](R|-)\d{2}',
                                '(\d{4}|\d{3})[A-Za-z]\d{3}([A-Za-z]|-)\d{3}',
                                '\d{2}[A-Za-z]\d{1}([A-Za-z]|-)\d{1}',
                                '\d{2}[A-Za-z]\d{1}(\.|\,)\d{2}([A-Za-z]|-)\d{1}',
                                '\d{2}(\.|\,)\d{1}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',                       
                                ' \d{1}(\.|\,)\d{2}(([A-Za-z]|-)|[A-Za-z]-)\d{2} ',
                                 ' \d{1}[A-Za-z]-\d{2} ',
                                '\d{3}[A-Za-z]\d{2}[A-Za-z]',
                                '\s\d{2}([A-Za-z]|-)\d{2}(\.|\,)\d{1}', 
                                '\d{2}[A-Za-z][A-Za-z]\d{2}', 
                                ]
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', str(row[cell.column-1].value))
                                    if result:
                                        tyresize_list.append(result.group(0))
                                        ### удаление среза с типоразмером и всем что написано перед типоразмером
                                        left_before_size_data_index = str(row[cell.column-1].value).index(result.group(0))
                                        if left_before_size_data_index > 0:
                                            str_left_data = str(row[cell.column-1].value)[0:left_before_size_data_index-1]
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(str_left_data, '')
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')

                            for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):    
                                ### проверка если строка пустая
                                if str(row[cell.column-1].value) is not str(row[cell.column-1].value):        
                                    tyremodel_list.append(' ')
                                ####### 
                                reg_list = ['BEL-\w+',
                                '(ФБел-\d{3}-\d{1})|(Бел-\d{3}-\d{1})|ФБел-\d{3}([A-Za-z]|[А-Яа-я])|(ФБел-\d{3})|(Бел-\d{2}(\.|\,)\d{2}(\.|\,)\d{2})|(Бел-\w+)|(Бел ПТ-\w+|ПТ-\w+)|(БелОШ\w+)',
                                #'БИ-\w+',
                                #'ВИ-\w+',
                                'И-\w+|ВИ-\w+|БИ-\w+',
                                '(Ф-\d{3}-\d{1})|(Ф-\d{2}[A-Za-z][A-Za-z]-\d{1})|(Ф-\d{2}\s[A-Za-z][A-Za-z]-\d{1})|(Ф-\d{2}-\d{1})|(Ф-\w+|КФ-\w+|ВФ-\w+)',
                                'ФД-\w+',
                                'ИД-\w+',
                                '(К|K)-\d{2}[А-Яа-я][А-Яа-я]',
                                '(В-\d{2}-\d{1})|(В-\w+|ИЯВ-\w+)',
                                'ФТ-\w+',
                                'Я-\w+',]   
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', str(row[cell.column-1].value))
                                    if result:
                                        #print(result.group(0))
                                        tyremodel_list.append(result.group(0))
                                        ### удаление среза с моделью
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')
                                        #print(str(row[cell.column-1].value))

                            for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):     
                                reg_list = [
                                    'ЗМШ',
                                    'КГШ',
                                    'Сер|сер|ср',
                                    'СГ',
                                    'Трп|Тр|Тпр',
                                    'Масс',
                                    'с/х|сх',
                                    'Лег|лг|легк', 
                                    'Груз|груз|гр',
                                    'Л/гр|Л/г|л/г',
                                    'бк|б/к',
                                    'Погр',
                                    'кам',
                                    'LS-2|LS|L-2',  
                                    'Type|Typ',
                                    'S|H|C',
                                    '((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2})[A-Za-z]))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2}))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1})|(\d{3}|\d{2})([А-Яа-я]|[A-Za-z]))', 
                                    'Газель',
                                    '(ВАЗ)',
                                    'Вездеход'
                                    'У-\d{1}',
                                    'ошип|а/к|выт|п/ош',
                                    '(ГК|ЕР)-\d{3}',
                                    'РК-5-165',
                                    '\(ак23.5\)|\(ол23.5\)|\(ГК-260\)|вен.260|\(РК-5А-145\)|\(о/л\)|о/л|\(кам.14.9\)|\(кам12,5\)|ЛК-35-16.5|\(ГК-165\)|\(вен.ТК\)|\(вен.161\)|вен.260|Подз|\(Подз\)|вен.|(о/л)|\(ЛК-35-16.5\)',
                                    '(кам.14.9)|(кам12,5)|вен.ЛК-35-16.5|ГК-145|РК.5-165',
                                    '(\d{2}|\d{1})+$',
                                ] 

                                list_of_parametrs = []
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', str(row[cell.column-1].value))                                  
                                    if result:
                                        list_of_parametrs.append(result.group(0))   
                                        #print('rEsUlT', result, print('N is =', n))
                                        ### удаление среза с моделью                                   
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')
                                    #################################### дополнительно получаем и формируем данные стандартых параметров НОРМ СЛОЙНОСТИ для добавления в словарь стандартых параметров dict_of_param_to_remake_in_standart    
                                    dict_ply = ''
                                    if n is '(\d{2}|\d{1})+$':
                                        if result:
                                            #print(n, 'НОРМА СЛОЙНОСТИ ПОЛУЧЕНА =', result.group(0))
                                            dict_ply = str(result.group(0))
                                            ply_dict[dict_ply] = result.group(0)
                                    ###########################
                                    #################################### дополнительно получаем и формируем данные индексов скорости нагрузки добавления в словарь стандартых параметров dict_of_param_to_remake_in_standart:    
                                    load_speed_index = ''
                                    if n is '((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2})[A-Za-z]))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2}))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1})|(\d{3}|\d{2})([А-Яа-я]|[A-Za-z]))':
                                        if result:
                                            #print(n, 'ИНДЕКС НАГРУЗКИ СКОРОСТИ ПОЛУЧЕН =', result.group(0))
                                            load_speed_index = str(result.group(0))
                                            load_speed_index_dict[load_speed_index] = result.group(0)
                                    ###########################
                                    pp = str(row[cell.column-1].value)                                      #### ????? это зачем - не задействовано ЖИ!
                                    #print(str(row[cell.column-1].value))    
                                        ### 
                                str_of_param = ' '.join(list_of_parametrs)
                                tyreparametrs_list.append(str_of_param)

                                
            ####### очистка списка параметров шины для формирования уникальных значений для справочника модели TyreParametersModel:                    
            tyreparametrs_list_cleaned = list(set(' '.join(tyreparametrs_list).split()))  

            #######################################################################################################################
            ################################# 2. модуль преобразователь - разные варианты написания к одному стандарту:

            ####### 2.1 преобразование уникальных параметров к стандарту для справочников:
            tyreparametrs_list_cleaned_and_prepared = []
            for n in (tyreparametrs_list_cleaned):
                for standart_dict_param in dict_of_param_to_remake_in_standart.keys():
                    if n in standart_dict_param:
                        n = dict_of_param_to_remake_in_standart.get(standart_dict_param)
                        tyreparametrs_list_cleaned_and_prepared.append(n)                                   # очищенные уникальные данные параметры для внесения в справочник
            ####### 2.2 преобразование параметров шины к стандарту для сопоставления с уникальными данными в справочниках в дальнейшем:
            #print(tyreparametrs_list)
            tyreparametrs_list_prepared = []
            for n in (tyreparametrs_list):
                tyre_params = ''.join(n).split()
                tyreparametrs_list_prepared.append(tyre_params)      

            ############################################################ Дополняет справочник стандартных dict_of_param_to_remake_in_standart новыми ключасми и значениями норм слойности из доп словаря ply_dict:
            dict_of_param_to_remake_in_standart.update(ply_dict)
            #print(dict_of_param_to_remake_in_standart)
            ############################################################
            ############################################################ Дополняет справочник стандартных dict_of_param_to_remake_in_standart новыми ключасми и значениями норм слойности из доп словаря load_speed_index_dict:
            dict_of_param_to_remake_in_standart.update(load_speed_index_dict)
            #print(dict_of_param_to_remake_in_standart)
            ############################################################

            #print('KK',tyreparametrs_list_prepared)       
            tyreparam_list = []    
            for tpl in tyreparametrs_list_prepared:
                tyreparametrs = []
                for n in tpl:
                    for standart_dict_param in dict_of_param_to_remake_in_standart.keys():
                        for standart_dict_param_value in standart_dict_param:
                            if n == standart_dict_param_value: 
                                #print('tyreparametr prepared=', n, 'standart_dict_param=', standart_dict_param)
                                for k in standart_dict_param:  
                                    if n == k:                                                                      #### ПРОВЕРКА НА ПОЛНОЕ соответстие с ключами dict_of_param_to_remake_in_standart для преобразования
                                        #print('n=', n, 'k=', k)
                                        n = dict_of_param_to_remake_in_standart.get(standart_dict_param)
                                        #print(n)
                                        tyreparametrs.append(n) 
                                        #print(tyreparametrs)
                    for k in list(ply_dict.values()):                                   # дополнительно провека норм слойности
                        if n == k: 
                            #print('n=',n, 'k=', k)
                            tyreparametrs.append(n)      
                    for k in list(load_speed_index_dict.values()):                                   # дополнительно провека Индексов нагрузки скорости
                        if n == k: 
                            #print('n=',n, 'k=', k)
                            tyreparametrs.append(n)         
                tyreparam_list.append(tyreparametrs)                                    # готовые данные параметры шины для сверки с справочником
            #print(tyreparametrs_list)
            #print(tyreparametrs_list_prepared)
            #print('tyreparam_list', tyreparam_list)                 

            #print(list(ply_dict.values()))

            ###################################### 3. Создать объекты справочников (ИНДЕКС СКОРОСТИ НАГРУЗИ И НОРМ СЛОЙНОСТИ ЗАКИДЫВАЮТСЯ ЗДЕСЬ ОТДЕЛЬНО):
            for tyre_model in tyremodel_list:
                dictionaries_models.ModelNameModel.objects.update_or_create(model=tyre_model)
                    
            for tyre_size in tyresize_list:
                dictionaries_models.TyreSizeModel.objects.update_or_create(tyre_size=tyre_size)

            for tyre_ply_value in ply_dict.values():
                dictionaries_models.TyreParametersModel.objects.update_or_create(tyre_type=tyre_ply_value)   

            for load_speed_index_value in load_speed_index_dict.values():
                dictionaries_models.TyreParametersModel.objects.update_or_create(tyre_type=load_speed_index_value)   
            
            for tyre_type in tyreparametrs_list_cleaned_and_prepared:
                dictionaries_models.TyreParametersModel.objects.update_or_create(tyre_type=tyre_type)   

            ##### сверка данных спарсенных с данными в справочниках:
            tyre_model_obj_list = []
            tyre_size_obj_list = []
            tyre_type_obj_list = []
            for n in dictionaries_models.ModelNameModel.objects.all():
                tyre_model_obj_list.append(n)
            for n in dictionaries_models.TyreSizeModel.objects.all():
                tyre_size_obj_list.append(n)
            for n in dictionaries_models.TyreParametersModel.objects.all():
                tyre_type_obj_list.append(n)

            tyre_model_list = [] 
            for cleaned_model_name in tyremodel_list:               # сверка спарсенных данных о модели с данными в БД справочнике модель
                for dict_ob in tyre_model_obj_list:
                    if cleaned_model_name == dict_ob.model:
                        #print(cleaned_model_name)
                        pass
                if cleaned_model_name is None:
                    cleaned_model_name = ''  
                tyre_model_list.append(cleaned_model_name)

            tyre_size_list = [] 
            for cleaned_tyresize_name in tyresize_list:               # сверка спарсенных данных о типоразмере с данными в БД справочнике типоразмер
                for dict_ob in tyre_size_obj_list:
                    if cleaned_tyresize_name == dict_ob.tyre_size:
                        #print(cleaned_tyresize_name)
                        pass
                if cleaned_tyresize_name is None:
                    cleaned_tyresize_name = ''                   
                tyre_size_list.append(cleaned_tyresize_name)

            #print('готовые данные параметры шины для сверки с справочником: tyreparam_list = ', tyreparam_list)
            tyre_param_list = []                                    # сверка спарсенных данных о параметрах шины с данными в БД справочнике параметры шины
            for cleaned_tyreparam_name in tyreparam_list:  
                trprmtrs = []   
                #print('ОТДЕЛЬНЫЙ ПОДСПИСОК парам готовые данные параметры шины для сверки с справочником', cleaned_tyreparam_name)          
                for n in cleaned_tyreparam_name:
                    #print('ОТДЕЛЬНЫЙ ЭЛЕМЕНТ ИЗ ОТДЕЛЬНЫЙ ПОДСПИСОК готовые данные параметры шины для сверки с справочником : n', n)
                    for dict_ob in tuple(tyre_type_obj_list):
                        #print('dict_ob ИЗ tyre_type_obj_list:', dict_ob.tyre_type)
                        if n == dict_ob.tyre_type:
                            #print('cleaned_tyreparam_name IS',cleaned_tyreparam_name)
                            #print('n = ', n, 'dict_ob.tyre_type = ', dict_ob.tyre_type)
                            trprmtrs.append(n)
                    if n is None:
                        n == ''
                        trprmtrs.append(n)
                tyre_param_list.append(trprmtrs)


            #print(tyre_model_list, len(tyre_model_list))
            #print(tyre_size_list, len(tyre_size_list))
            #print('tyre_param_list ==', tyre_param_list, len(tyre_param_list))
                ###### запись в модель Tyre данных о модели типоразмере и параметрах - сверенных с данными в моделях справочников
            if len(tyre_model_list) == len(tyre_size_list) and len(tyre_model_list) == len(tyre_param_list):                ########### ЗДЕСЬ ВРОДЬ КАК ДАННЫЕ ЧТО ПОЙДУТ В МОДЕЛЬ TYRE
                for n in range(0, len(tyre_param_list)):
                    ######################################  Проверяем, существует ли в БД уже объект шина с заданными параметрами:
                    mod_pos = tyre_model_list[n]
                    size_pos = tyre_size_list[n]
                    param_pos = tyre_param_list[n]
                    tyre_obj_exist = tyres_models.Tyre.objects.filter(tyre_model__model=mod_pos, tyre_size__tyre_size=size_pos, tyre_type__tyre_type__in=param_pos)
                    ######################################  
                for n in range(0, len(tyre_param_list)):
                    tyre_type_el_list = []
                    for k in range (0, len(tyre_param_list[n])):
                        tyre_type_el = dictionaries_models.TyreParametersModel.objects.get(tyre_type=tyre_param_list[n][k])
                        #print(tyre_type_el)
                        tyre_type_el_list.append(tyre_type_el)
                    if tyre_obj_exist:                              ### если объект существует - не созавать новый такой же
                        #print('YEAP!', tyre_obj_exist)
                        pass          
                    else:
                        #print('tyre_type_el_list = ', tyre_type_el_list)           
                        tyre_obj = tyres_models.Tyre.objects.create(                                                        ####  СОЗДАЕМ объект Tyre
                            tyre_model=dictionaries_models.ModelNameModel.objects.get(model=tyre_model_list[n]),
                            tyre_size=dictionaries_models.TyreSizeModel.objects.get(tyre_size=tyre_size_list[n]), 
                        )
                        for n in tyre_type_el_list:
                            tyre_obj.tyre_type.add(n)

                        #tyre_obj = tyres_models.Tyre.objects.update_or_create(
                        #    tyre_model=dictionaries_models.ModelNameModel.objects.get(model=tyre_model_list[n]),
                        #    tyre_size=dictionaries_models.TyreSizeModel.objects.get(tyre_size=tyre_size_list[n]), 
                        #    ##tyre_type=dictionaries_models.TyreParametersModel.objects.get(tyre_type=tyre_type_el.tyre_type),
                        #)
                        #print('tyre_obj = ', tyre_obj, type(tyre_obj))
                        #for n in tyre_type_el_list:
                        #    tyre_obj[0].tyre_type.add(n)
            
            ### Создать или проверить наличие групп шин:
            group_names = ['легковые', 'легкогруз', 'с/х', 'грузовые']
            for group_name in group_names:
                dictionaries_models.TyreGroupModel.objects.get_or_create(
                    tyre_group=group_name
                )
            #for obj in dictionaries_models.TyreGroupModel.objects.all():
            #    print(obj, obj.tyre_group)

            ###  
            for obj in tyres_models.Tyre.objects.all():
                for p in obj.tyre_type.all():
                    if p.tyre_type == 'груз':
                        group_obect = dictionaries_models.TyreGroupModel.objects.get(tyre_group='грузовые')
                        obj.tyre_group.add(group_obect)
                    elif p.tyre_type == 'легк':
                        group_obect = dictionaries_models.TyreGroupModel.objects.get(tyre_group='легковые')
                        obj.tyre_group.add(group_obect)
                    elif p.tyre_type == 'сх':
                        group_obect = dictionaries_models.TyreGroupModel.objects.get(tyre_group='с/х')
                        obj.tyre_group.add(group_obect)
                    elif p.tyre_type == 'л/г':
                        group_obect = dictionaries_models.TyreGroupModel.objects.get(tyre_group='легкогруз')
                        obj.tyre_group.add(group_obect)

            ####################################################### Запись данных в файл
            from openpyxl import Workbook
            excel_file = Workbook()
            excel_sheet = excel_file.create_sheet(title='Holidays 2019', index=0)
            excel_sheet['A1'] = 'Типоразмер'
            excel_sheet['B1'] = 'Модель'
            excel_sheet['C1'] = 'Параметры'
            for n in range(0, tyres_models.Tyre.objects.all().count()):
                obj = tyres_models.Tyre.objects.all()[n]
                tyresize_val = obj.tyre_model.model
                tyremodel_val = obj.tyre_size.tyre_size
                tyreparmetrs_val_list = []
                for qo in obj.tyre_type.all():
                    tyreparmetrs_val = qo.tyre_type
                    tyreparmetrs_val_list.append(tyreparmetrs_val)
                tyreparametrs_val = ' '.join(tyreparmetrs_val_list) 
                excel_sheet.cell(row=n+1, column=1).value = tyresize_val
                excel_sheet.cell(row=n+1, column=2).value = tyremodel_val
                excel_sheet.cell(row=n+1, column=3).value = tyreparametrs_val
                #for n in range(len(tyresize_list)): 
                #    excel_sheet.cell(row=n+1, column=1).value = tyresize_list[n]
                #for n in range(len(tyremodel_list)): 
                #    excel_sheet.cell(row=n+1, column=2).value = tyremodel_list[n]
                #for n in range(len(tyreparametrs_list)): 
                #    excel_sheet.cell(row=n+1, column=3).value = tyreparametrs_list[n]     
        
            #for n in range(len(pp)): 
            #    excel_sheet.cell(row=n+1, column=4).value = pp[n]                         
            excel_file.save(filename="Tyres.xlsx")
    ############################################################
            form = forms.ImportDataForm()
            return render(self.request, 'filemanagment/excel_import.html', {'form': form})            


        #########################################################################
        ### ЕСЛИ ЗАБРАСЫВАЮТСЯ ФАЙЛЫ С ДАННЫМИ О ПРОДАЖАХ/ОСТАТКАХ/ПРОИЗВОДСТВЕ/ЦЕНЫ:
        ################ считывание файла и сопоставление с текущей базой данных


        elif form_name == "bform.prefix":
            form = forms.ImportSalesDataForm(self.request.POST, self.request.FILES)  
            if form.is_valid():
                file_to_read = openpyxl.load_workbook(self.request.FILES['file_fields'], data_only=True)     
                sheet = file_to_read['Sheet1']      # Читаем файл и лист1 книги excel 
                for row in sheet.rows:                      
                    for cell in row:
                        if cell.value == 'контрагент':          # получаем колонку 'контрагент'
                            contragent_column = cell.column
                            contragent_row = cell.row
                            for col in sheet.iter_cols(min_row=contragent_row+1, min_col=contragent_column, max_col=contragent_column, max_row=sheet.max_row):
                                for cell in col:
                                    contragent_value = ''
                                    contragent_value =  cell.value                               
                                    contragent_list.append(contragent_value)

                        # 1 Парсинг
                        if cell.value == 'дата':        # получаем строку'дата'
                            #print(cell.value)    
                            #print(cell.coordinate) 
                            cell = sheet.cell(row=cell.row+1, column=cell.column)
                            column_sell_date = cell.value
                            date_period = column_sell_date                      # ЗДЕСЬ ПОЛУЧЕНА ДАТА ДЛЯ СЕБЕСТОИМОСТИ И ПРАЙСОВ


                        elif cell.value == 'объем продаж':
                            saless_row_temp = int
                            #sales_column = cell.coordinate          # получаем колонку 'объем продаж'
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value                            
                                    sales_list.append(sell_value)

                                    #print('saless_row', saless_row, 'current_row_number', current_row_numberr, cell.row)
                                    saless_row_dict[cell.row] = sell_value                                                      # закидываем в словарь строка значение объем продаж

                                    pass       
                            sales_list = [float(x) for x in sales_list]    # str значения в float

                        elif cell.value == 'Полные затраты':
                            #sales_column = cell.coordinate          # получаем колонку 'полные затраты'    planned_costs
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        #print('cell.value.lstrip().rstrip()', cell.value.lstrip().rstrip() )
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value  
                                    if sell_value is None:
                                        pass
                                    else:
                                        if type(sell_value) is str:
                                            sell_value = 0                                       
                                        planned_costs.append(sell_value)
                                        planned_costs_row_dict[cell.row] = sell_value                                                      # закидываем в словарь строка значение 
                                    pass
                            #print(planned_costs)
                            planned_costs = [float(x) for x in planned_costs]    # str значения в float

                        elif cell.value == 'прямые затраты':
                            #sales_column = cell.coordinate          # получаем колонку 'прямые затраты'    semi_variable_costs
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value   
                                    if sell_value is None:
                                        pass
                                    else:
                                        if type(sell_value) is str:
                                            sell_value = 0                          
                                        semi_variable_costs.append(sell_value)

                                        semi_variable_costs_row_dict[cell.row] = sell_value                                                      # закидываем в словарь строка значение 

                                    pass
                            #print(semi_variable_costs)
                            semi_variable_costs = [float(x) for x in semi_variable_costs]    # str значения в float
                            #print(semi_variable_costs)

                        elif cell.value == 'прейскуранты №№9, 902':
                            #sales_column = cell.coordinate          # получаем колонку 'прейскуранты №№9, 902'    belarus902price_costs
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value
                                    if sell_value is None:
                                        pass
                                    else:
                                        if type(sell_value) is str:
                                            sell_value = 0                              
                                        belarus902price_costs.append(sell_value)

                                        belarus902price_costs_row_dict[cell.row] = sell_value                                                      # закидываем в словарь строка значение 

                                    pass
                            belarus902price_costs = [float(x) for x in belarus902price_costs]    # str значения в float
                            #print(belarus902price_costs)

                        elif cell.value == 'ТПС РФ FCA':
                            #sales_column = cell.coordinate          # получаем колонку 'ТПС РФ FCA'    tpsrussiafcaprice
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value
                                    if sell_value is None:
                                        pass
                                    else:
                                        if type(sell_value) is str:
                                            sell_value = 0                              
                                        tpsrussiafcaprice_costs.append(sell_value)

                                        tpsrussiafcaprice_costs_row[cell.row] = sell_value                                                      # закидываем в словарь строка значение 

                                    pass
                            tpsrussiafcaprice_costs = [float(x) for x in tpsrussiafcaprice_costs]    # str значения в float
                            #print(tpsrussiafcaprice_costs)

                        elif cell.value == 'ТПС Казахстан FCA':
                            #sales_column = cell.coordinate          # получаем колонку 'ТПС Казахстан FCA'    tpskazfcaprice
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value
                                    if sell_value is None:
                                        pass
                                    else:
                                        if type(sell_value) is str:
                                            sell_value = 0                              
                                        tpskazfcaprice_costs.append(sell_value)

                                        tpskazfcaprice_cost_row[cell.row] = sell_value                                                      # закидываем в словарь строка значение 

                                    pass
                            tpskazfcaprice_costs = [float(x) for x in tpskazfcaprice_costs]    # str значения в float
                            #print('tpskazfcaprice_costs', tpskazfcaprice_costs)

                        elif cell.value == 'ТПС Средняя Азия, Закавказье, Молдова FCA':
                            #sales_column = cell.coordinate          # получаем колонку 'ТПС Средняя Азия, Закавказье, Молдова FCA'    tpsmiddleasiafcaprice
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value
                                    if sell_value is None:
                                        pass
                                    else:
                                        if type(sell_value) is str:
                                            sell_value = 0                              
                                        tpsmiddleasiafcaprice_costs.append(sell_value)

                                        tpsmiddleasiafcaprice_costs_row[cell.row] = sell_value                                                      # закидываем в словарь строка значение 

                                    pass
                            tpsmiddleasiafcaprice_costs = [float(x) for x in tpsmiddleasiafcaprice_costs]    # str значения в float
                            #print(tpsmiddleasiafcaprice_costs)

                        elif cell.value == 'Действующие цены':
                            #sales_column = cell.coordinate          # получаем колонку 'Действующие цены'   
                            sales_column = cell.column
                            sales_row = cell.row
                            for col in sheet.iter_cols(min_row=sales_row+1, min_col=sales_column, max_col=sales_column, max_row=sheet.max_row):
                                for cell in col:
                                    sell_value = ''
                                    #sell_value =  cell.value.lstrip().rstrip().replace('.', ',')      # убрать пробелы в начале строки и в конце строки  
                                    if sell_value is str:
                                        sell_value = cell.value.lstrip().rstrip()   
                                    else:
                                        sell_value = cell.value
                                    if sell_value is None:
                                        pass
                                    else:
                                        if type(sell_value) is str:
                                            sell_value = 0                              
                                        current_prices.append(sell_value)

                                        current_prices_row[cell.row] = sell_value                                                      # закидываем в словарь строка значение 

                                    pass
                            current_prices = [float(x) for x in current_prices]    # str значения в float
                            #print(current_prices)
                            #print('current_prices_row', current_prices_row)
                        
                        
                        ##  ПОЛУЧЕНИЕ МОДЕЛИ ТИПОРАЗМЕРА и ТИПА ДЛЯ ФОРМИРОВАНИЯ СЛОВАРЯ И СВЕРКИ СОСПАВШИХ ШИН ИЗ БД ДЛЯ ВЫБОРКИ ДАННЫХ ПРДАЖИ И МИНИМАЛКИ И ПР ИЗ ЭТОЙ СТРОКИ  !!!!!!!!!!!
                        ##

                        current_row_number = int

                        if cell.value == 'Наименование продукции':
                            for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):   
                                #print('Row number:', str(row[0].row),'ROW ROW ROW')                         # СПОСОБ ПОЛУЧИТЬ НОМЕР СТРОКИ
                         
                                ### проверка если строка пустая
                                if str(row[cell.column-1].value) is not str(row[cell.column-1].value):        
                                    tyresize_list.append(' ')
                                #######
                                reg_list = [
                                #'\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2})', 
                                #'\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2}', 
                                #'(\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2})',  # = '(\d{3}|\d{2})/\d{2}([A-Za-z]|-)\d{2}' +  '\d{3}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',    
                                '(\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}))|(\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2})|((\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2}))', #3 в одном чтобы избежать повторений двойных в ячейке наподобие #АШ 480/80R42(18.4R42)
                                '\d{2}(\.|\,)\d{1}[A-Za-z](R|-)\d{2}',
                                '(\d{4}|\d{3})[A-Za-z]\d{3}([A-Za-z]|-)\d{3}',
                                '\d{2}[A-Za-z]\d{1}([A-Za-z]|-)\d{1}',
                                '\d{2}[A-Za-z]\d{1}(\.|\,)\d{2}([A-Za-z]|-)\d{1}',
                                '\d{2}(\.|\,)\d{1}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',                       
                                ' \d{1}(\.|\,)\d{2}(([A-Za-z]|-)|[A-Za-z]-)\d{2} ',
                                 ' \d{1}[A-Za-z]-\d{2} ',
                                '\d{3}[A-Za-z]\d{2}[A-Za-z]',
                                '\s\d{2}([A-Za-z]|-)\d{2}(\.|\,)\d{1}', 
                                '\d{2}[A-Za-z][A-Za-z]\d{2}', 
                                ]
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', str(row[cell.column-1].value))
                                    if result:
                                        #print('result.group(0)', result.group(0))
                                        tyresize_list.append(result.group(0))
                                        tyretype_row_dict[row[0].row] = result.group(0)                                     # закидываем в словарь строка значение 
                                        #print(row[0].row, 'cell.row', result.group(0), 'result.group(0)')
                                        ### удаление среза с типоразмером и всем что написано перед типоразмером
                                        left_before_size_data_index = str(row[cell.column-1].value).index(result.group(0))
                                        if left_before_size_data_index > 0:
                                            str_left_data = str(row[cell.column-1].value)[0:left_before_size_data_index-1]
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(str_left_data, '')
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')

                            for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):    
                                ### проверка если строка пустая
                                if str(row[cell.column-1].value) is not str(row[cell.column-1].value):        
                                    tyremodel_list.append(' ')
                                ####### 
                                reg_list = ['BEL-\w+',
                                '(ФБел-\d{3}-\d{1})|(Бел-\d{3}-\d{1})|ФБел-\d{3}([A-Za-z]|[А-Яа-я])|(ФБел-\d{3})|(Бел-\d{2}(\.|\,)\d{2}(\.|\,)\d{2})|(Бел-\w+)|(Бел ПТ-\w+|ПТ-\w+)|(БелОШ\w+)',
                                #'БИ-\w+',
                                #'ВИ-\w+',
                                'И-\w+|ВИ-\w+|БИ-\w+',
                                '(Ф-\d{3}-\d{1})|(Ф-\d{2}[A-Za-z][A-Za-z]-\d{1})|(Ф-\d{2}\s[A-Za-z][A-Za-z]-\d{1})|(Ф-\d{2}-\d{1})|(Ф-\w+|КФ-\w+|ВФ-\w+)',
                                'ФД-\w+',
                                'ИД-\w+',
                                '(К|K)-\d{2}[А-Яа-я][А-Яа-я]',
                                '(В-\d{2}-\d{1})|(В-\w+|ИЯВ-\w+)',
                                'ФТ-\w+',
                                'Я-\w+',]   
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', str(row[cell.column-1].value))
                                    if result:
                                        #print(result.group(0), 'result.group(0)')
                                        tyremodel_list.append(result.group(0))
                                        model_row_dict[row[0].row] = result.group(0)        # закидываем в словарь строка значение 
                                        model_row = result.group(0)
                                        ### удаление среза с моделью
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')
                                        #print(str(row[cell.column-1].value))

                            for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):     
                                reg_list = [
                                    'ЗМШ',
                                    'КГШ',
                                    'Сер|сер|ср',
                                    'СГ',
                                    'Трп|Тр|Тпр',
                                    'Масс',
                                    'с/х|сх',
                                    'Лег|лг|легк', 
                                    'Груз|груз|гр',
                                    'Л/гр|Л/г|л/г',
                                    'бк|б/к',
                                    'Погр',
                                    'кам',
                                    'LS-2|LS|L-2',  
                                    'Type|Typ',
                                    'S|H|C',
                                    '((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2})[A-Za-z]))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2}))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1})|(\d{3}|\d{2})([А-Яа-я]|[A-Za-z]))', 
                                    'Газель',
                                    '(ВАЗ)',
                                    'Вездеход'
                                    'У-\d{1}',
                                    'ошип|а/к|выт|п/ош',
                                    '(ГК|ЕР)-\d{3}',
                                    'РК-5-165',
                                    '\(ак23.5\)|\(ол23.5\)|\(ГК-260\)|вен.260|\(РК-5А-145\)|\(о/л\)|о/л|\(кам.14.9\)|\(кам12,5\)|ЛК-35-16.5|\(ГК-165\)|\(вен.ТК\)|\(вен.161\)|вен.260|Подз|\(Подз\)|вен.|(о/л)|\(ЛК-35-16.5\)',
                                    '(кам.14.9)|(кам12,5)|вен.ЛК-35-16.5|ГК-145|РК.5-165',
                                    '(\d{2}|\d{1})+$',
                                ]                
                                list_of_parametrs = []
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', str(row[cell.column-1].value)) 
                                    if result:
                                        list_of_parametrs.append(result.group(0)) 
                                        #print(row[0].row, result.group(0), type(result.group(0)))
                                        params_row_dict[row[0].row] = list_of_parametrs           # закидываем в словарь строка значение 
                                        #print('rEsUlT', result, print('N is =', n))
                                        ### удаление среза с моделью                                   
                                        row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')
                                    #################################### дополнительно получаем и формируем данные стандартых параметров НОРМ СЛОЙНОСТИ для добавления в словарь стандартых параметров dict_of_param_to_remake_in_standart    
                                    dict_ply = ''
                                    if n is '(\d{2}|\d{1})+$':
                                        if result:
                                            #print(n, 'НОРМА СЛОЙНОСТИ ПОЛУЧЕНА =', result.group(0))
                                            dict_ply = str(result.group(0))
                                            ply_dict[dict_ply] = result.group(0)
                                    ###########################
                                    #################################### дополнительно получаем и формируем данные индексов скорости нагрузки добавления в словарь стандартых параметров dict_of_param_to_remake_in_standart:    
                                    load_speed_index = ''
                                    if n is '((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2})[A-Za-z]))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2}))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1})|(\d{3}|\d{2})([А-Яа-я]|[A-Za-z]))':
                                        if result:
                                            #print(n, 'ИНДЕКС НАГРУЗКИ СКОРОСТИ ПОЛУЧЕН =', result.group(0))
                                            load_speed_index = str(result.group(0))
                                            load_speed_index_dict[load_speed_index] = result.group(0)
                                    ###########################
                                    pp = str(row[cell.column-1].value)                                      #### ????? это зачем - не задействовано ЖИ!
                                    #print(str(row[cell.column-1].value))    
                                        ### 
                                str_of_param = ' '.join(list_of_parametrs)
                                tyreparametrs_list.append(str_of_param)
                                #print(str_of_param, 'str_of_param')


                ############################################################ Дополняет справочник стандартных dict_of_param_to_remake_in_standart новыми ключасми и значениями норм слойности из доп словаря ply_dict:
                dict_of_param_to_remake_in_standart.update(ply_dict)
                #print(dict_of_param_to_remake_in_standart)
                ############################################################
                ############################################################ Дополняет справочник стандартных dict_of_param_to_remake_in_standart новыми ключасми и значениями норм слойности из доп словаря load_speed_index_dict:
                dict_of_param_to_remake_in_standart.update(load_speed_index_dict)
                #print(dict_of_param_to_remake_in_standart)
                ############################################################
                # ПРЕОБРАЗОВАНИЕ СПАРСЕННЫХ ДАННЫХ В ВИД ПО БД   + при этом далее есть еще старый код по преобразованию не словаря а списка всех значений
                for keys, values in params_row_dict.items():
                    #print(keys, values)
                    tyreparametrs_list_clean = []
                    for n in (values):
                        tyre_el = sorted(n.split(' '), reverse=True)
                        tyreparametrs_list_cleaned_and_prepared = []
                        for el_in_param in tyre_el:
                            for standart_dict_param in dict_of_param_to_remake_in_standart.keys():
                                #print('HHHHHHHHH', type(tuple(standart_dict_param)), standart_dict_param)           ###### str значения словаря в тапл
                                if el_in_param in list(standart_dict_param) or el_in_param == standart_dict_param: 
                                    #print('el_in_param = ', el_in_param, 'standart_dict_param = ', standart_dict_param)      #!!!!!!!!!!!!!!!!
                                    el_in_param = dict_of_param_to_remake_in_standart.get(standart_dict_param)
                                    tyreparametrs_list_cleaned_and_prepared.append(el_in_param)  
                            el = ' '.join(tyreparametrs_list_cleaned_and_prepared) 
                        tyreparametrs_list_clean.append(el)  
                    params_row_dict[keys] = tyreparametrs_list_clean
                #

                ##print(row_parsing_dict)
                #print('tyretype_row_dict', len(tyretype_row_dict))
                #print('model_row_dict', len(model_row_dict))
                #print('model_row_dict', len(params_row_dict), params_row_dict)
                #print('saless_row_dict',len(saless_row_dict)) 
                #print('planned_costs_row_dict ', len(planned_costs_row_dict))  
                #print('semi_variable_costs_row_dict', len(semi_variable_costs_row_dict))   
                #print('belarus902price_costs_row_dict', len(belarus902price_costs_row_dict))   
                #print('tpsrussiafcaprice_costs_row', len(tpsrussiafcaprice_costs_row) )                                        
                #print('tpskazfcaprice_cost_row', len(tpskazfcaprice_cost_row))  
                #print('tpsmiddleasiafcaprice_costs_row', len(tpsmiddleasiafcaprice_costs_row))  

                #r_item = ' '
                #for item in tyresize_list:
                #    if item == r_item:
                #        tyresize_list.remove(item)
                #
#
                #print(len(tyresize_list), 'tyresize_list', tyresize_list)           
                #print(len(tyresize_list), 'tyresize_list', tyresize_list)    
                #print(len(tyremodel_list), 'tyremodel_list')
                #print(len(tyreparametrs_list), 'tyreparametrs_list')  
                #print(len(tpsmiddleasiafcaprice_costs), 'tpsmiddleasiafcaprice_costs')
                #print(len(tpskazfcaprice_costs), 'tpskazfcaprice_costs') 
                #print(len(tpsrussiafcaprice_costs), 'tpsrussiafcaprice_costs')
                #print(len(belarus902price_costs), 'belarus902price_costs')
                #print(len(semi_variable_costs), 'semi_variable_costs')
                #print(len(planned_costs), 'planned_costs')
                

            ############################################################ Дополняет справочник стандартных dict_of_param_to_remake_in_standart новыми ключасми и значениями норм слойности из доп словаря ply_dict:
            dict_of_param_to_remake_in_standart.update(ply_dict)
            #print(dict_of_param_to_remake_in_standart)
            ############################################################
            ############################################################ Дополняет справочник стандартных dict_of_param_to_remake_in_standart новыми ключасми и значениями норм слойности из доп словаря load_speed_index_dict:
            dict_of_param_to_remake_in_standart.update(load_speed_index_dict)
            #print(dict_of_param_to_remake_in_standart)
            ############################################################


            ####### 2. преобразование параметров шины к стандарту для сопоставления с уникальными данными в справочниках в дальнейшем:
            tyreparametrs_list_cleaned_and_prepared_ready = []                  # список параметов шины из таблицы подготовленных для сопоставления с базой
            for n in (tyreparametrs_list):
                tyre_el = sorted(n.split(' '), reverse=True)
                tyreparametrs_list_cleaned_and_prepared = []
                for el_in_param in tyre_el:
                    for standart_dict_param in dict_of_param_to_remake_in_standart.keys():
                        #print('HHHHHHHHH', type(tuple(standart_dict_param)), standart_dict_param)           ###### str значения словаря в тапл
                        if el_in_param in list(standart_dict_param) or el_in_param == standart_dict_param: 
                            #print('el_in_param = ', el_in_param, 'standart_dict_param = ', standart_dict_param)      #!!!!!!!!!!!!!!!!
                            el_in_param = dict_of_param_to_remake_in_standart.get(standart_dict_param)
                            tyreparametrs_list_cleaned_and_prepared.append(el_in_param)  
                    el = ' '.join(tyreparametrs_list_cleaned_and_prepared)                   
                tyreparametrs_list_cleaned_and_prepared_ready.append(el)  # список параметов шины из таблицы подготовленных для сопоставления с базой
                
            tyre_param_list_from_db = dictionaries_models.TyreParametersModel.objects.all()
            tyre_param_list_from_db_param_only = []
            for n in tyre_param_list_from_db:
                tyre_param_list_from_db_param_only.append(n.tyre_type)              #####! спикок уникальных имет параметров шины из базы данных

            #print('данные из БД перечень:', tyre_param_list_from_db_param_only)      
            #print('исходные данные:', tyreparametrs_list)             
            #print('подготовленные для сверки с бд:', tyreparametrs_list_cleaned_and_prepared_ready) 
        
            ######### 3 Сопоставление - сверка данных из таблицы с параметами в БД
            
            #print(tyreparametrs_list_cleaned_and_prepared_ready)
            #print(tyre_param_list_from_db_param_only)
            tyreparam_list = []                                                     # ПОДГОТОВЛЕНЫЫЙ И ОЧИЩЕННЫЙ СПИСОК ДАННЫХ ПАРАМЕТРОВ ШИНЫ ДЛЯ СОПОСТАВЛЕНИЯ С БД НА ФИНАЛЬНОЙ СТАДИИ ВНЕСЕНИЯ (реализац/остатки/произв) в Базу  
            tyreparam_list_with_lists = []                                             # ПОДГОТОВЛЕНЫЫЙ И ОЧИЩЕННЫЙ СПИСОК ДАННЫХ ПАРАМЕТРОВ ШИНЫ в виде вложенных списков ДЛЯ СОПОСТАВЛЕНИЯ С БД НА ФИНАЛЬНОЙ СТАДИИ ВНЕСЕНИЯ (реализац/остатки/произв) в Базу  
            for tpl in tyreparametrs_list_cleaned_and_prepared_ready:
                tyre_params_value = []
                tpl_list = sorted(tpl.split(' '), reverse=True)
                for n in tpl_list:  # sorted(GG.split(' '), reverse=True)   
                    for standart_dict_param in tyre_param_list_from_db_param_only:
                        if n == standart_dict_param:
                        #if n in standart_dict_param:
                            tyre_params_value.append(n)
                tyre_params_value_str = ', '.join(tyre_params_value)                    ## !!!! Для формирования списка со строками 

                tyreparam_list.append(tyre_params_value_str)  
                tyreparam_list_with_lists.append(tyre_params_value) 
            #print(len(tyreparam_list), tyreparam_list)                               # совпавшие данные параметры шины из таблицы с параметрами в БД
            #print(len(tyresize_list), tyresize_list)
            #print(len(tyremodel_list), tyremodel_list)

            #print(len(tyreparam_list_with_lists), tyreparam_list_with_lists)

            ##### Запись в модель данных (например, о продажах):

            #### Проверка - вывод в файл данных
            #if len(tyresize_list) == len(tyremodel_list) and len(tyresize_list) ==  len(tyreparametrs_list):
            #    for n in range(0, len(tyresize_list)):
            #        #if tyresize_list[n] == tyres_models.Tyre.objects.filter(tyre_size__tyre_size=tyresize_list[n]) and tyremodel_list[n] == tyres_models.Tyre.objects.filter(tyre_model__model=tyremodel_list[n]) and tyreparametrs_list[n] == tyres_models.Tyre.objects.filter(tyre_type__tyre_type=tyreparametrs_list[n]):
            #        some_list = tyres_models.Tyre.objects.filter(tyre_size__tyre_size__icontains='315/80R22.5')
            #        print(some_list, tyresize_list[n], tyres_models.Tyre.objects.get(id=2).tyre_size)

            ###################################### СВЕРКА СПИСКОВ МОДЕЛЬ ТИПОРАЗМЕР ПАРАМЕТРЫ с ДАННЫМИ В МОДЕЛИ ШИНЫ В БД  + внесение данныхв в одель Sales(Например):
            #print(len(tyresize_list), tyresize_list)           # 1   
            #print(len(tyremodel_list), tyremodel_list)         # 2
            #print(len(tyremodel_list), tyreparam_list)          # 3/1  в виде списка со строками
            ##print(len(tyreparam_list_with_lists), tyreparam_list_with_lists)    # 3/2  в виде списка с вложенными списками
#
            #print(len(tyresize_list), 'tyresize_list')           # 1   
            #print(len(tyremodel_list), 'tyremodel_list')         # 2
            #print(len(tyremodel_list), 'tyreparam_list')          # 3/1  в виде списка со строками

            #print('SALES', len(sales_list), sales_list)
            #print(tyres_models.Tyre.objects.get(tyre_type__tyre_type__contains='сер'))
            #print(tyres_models.Tyre.objects.filter(tyre_type__tyre_type__in=tyreparam_list_with_lists[2]))
            tyre_obj_list = []
            sale_obj_list = []
            object_list_finel = []


            #### прокладка: уберем запятые из строк с параметрами:
            #print('TTT', tyreparam_list)
            t_list = []
            for n in tyreparam_list:
                temporaly_list = []
                param = str(n)
                n = param.replace(',', '')
                temporaly_list = n
                t_list.append(temporaly_list)
            tyreparam_list = t_list
            #print('TTT',tyreparam_list)
            ####

            ######################################                      ВАРИАНТ  1  =  СОПОСТАВЛЕНИЕ СОВПАШИХ ШИН С БД

            list_of_unique_tyres_objs_cleaned = []
            #print(tyreparam_list)
            if len(tyresize_list) == len(tyremodel_list) and len(tyremodel_list) == len(tyreparam_list):
                for n in range(0, len(tyreparam_list)):
                    ######################################  Проверяем, существует ли в БД уже объект шина с заданными параметрами:
                    mod_pos = tyremodel_list[n]
                    size_pos = tyresize_list[n]
                    param_pos = tyreparam_list[n]
                    #print(mod_pos, size_pos, param_pos)
                    param_pos_list = sorted(tyreparam_list[n].split(' '), reverse=True)
                    #print(param_pos_list)
                    tyre_obj_exist = tyres_models.Tyre.objects.filter(tyre_model__model=mod_pos, tyre_size__tyre_size=size_pos, tyre_type__tyre_type__in=param_pos_list)
                    if tyre_obj_exist:                              ### если кверисет объектов существует
                        #print('YEAP!', tyre_obj_exist)
                    #print('_____________')
                        list_of_unique_tyres_objs = []
                        for obj in tyre_obj_exist:              ### берем объекты из кверисета
                            #print('param=',param, 'obj.tyre_type.all() = ', obj.tyre_type.all())
                            counter_coinc = 0
                            for param in param_pos_list:                ### берем параметры из param_pos_list и перебираем
                                len(param_pos_list)                     ###  замеряем количество параметров в текущем param_pos_list 
                                #print(len(param_pos_list))
                                for p in obj.tyre_type.all():       ###   перебираем параметры из param_pos_list в параметрах объекта
                                    #print('param = ', param , 'p.tyre_type = ', p.tyre_type)
                                    if param == p.tyre_type:        ### если параметры совпадают
                                        #print('param = ', param, 'p.tyre_type = ', p.tyre_type)
                                        counter_coinc += 1
                            if counter_coinc == len(param_pos_list):        ###### ЗДЕСЬ ПОЛУЧАЕМ ОБЪЕКТ У КОТОРОГО ВСЕ ПАРАМЕТРЫ СОВПАЛИ СПАРАМЕТРАМИ ШИНЫ В БАЗЕ
                                ##################print(obj)
                                list_of_unique_tyres_objs.append(obj)
                        list_of_unique_tyres_objs_cleaned.append(list(set(list_of_unique_tyres_objs)))
                    #print('_____________')
            #print(list_of_unique_tyres_objs_cleaned, len(list_of_unique_tyres_objs_cleaned))        ####!!!!!! СПИСОК С ОБЪЕКТАМИ с СОВПАВШИМИ ПАРАМЕТРАМИ - итоговые даннее готовые

            #### ВСТАВКА:
            ##### + Создаем единую таблицу SALES_TABLE:                                                
            sales_table, created = sales_models.SalesTable.objects.get_or_create()                   ##### !!!!!  ####### ДЛЯ РАБОТЫ С СТРАНИЦЕЙ SALES:    
            #### КОНЕЦ ВСТАВКИ  

            ### ЗДЕСЬ ПОНАДОБИТСЯ ДАЛЬШЕ когда получим нужный объект:
            #print(list_of_unique_tyres_objs_cleaned)
            sales_list_values_list = sales_list
            for obj_list_el in list_of_unique_tyres_objs_cleaned:
                row_value_counter = 0
                #print(obj_list_el)

                # Дата продаж
                if column_sell_date:
                    #print(type(column_sell_date))
                    #date_time_obj = datetime.strptime(column_sell_date, '%Y/%m/%d')
                    #sell_date = date_time_obj
                    sell_date = column_sell_date
                else:
                    sell_date =  datetime.today()
                # Объемы продаж
                if sales_list_values_list:
                    n = sales_list_values_list.pop(0)
                else:
                    n = 2
                # Контрагенты:
                #print(contragent_list, 'contragent_list')
                # Создадим контрагента:
                contragent = ' '
                if contragent_list:
                    contragent = contragent_list.pop(0)
                    #contragent_name = 'БНХ РОС'
                    if contragent is None:
                        contragent = 'нет данных'
                        dictionaries_models.ContragentsModel.objects.get_or_create(
                            contragent_name = contragent
                            ) 
                    if contragent:
                        dictionaries_models.ContragentsModel.objects.get_or_create(
                            contragent_name = contragent
                            )
                    #else:
                    #    contragent = ' '
                    #    dictionaries_models.ContragentsModel.objects.get_or_create(
                    #        contragent_name = contragent
                    #        )
                else:
                    contragent = 'нет данных'
                    dictionaries_models.ContragentsModel.objects.get_or_create(
                        contragent_name = contragent
                        )  
                #dictionaries_models.ContragentsModel.objects.get_or_create(
                #    contragent_name = 'БНХ РОС'
                #    )
                         
                for obj in obj_list_el:
                #    ############################################################################################################################
                            #print(obj.tyre_model.model, obj.tyre_size.tyre_size)       # проверка совпавших параметров
                #    course_qs = obj.tyre_type.all()                                                         # проверка совпавших параметров
                #    for course in course_qs:                                                                    # проверка совпавших параметров
                #        print(course.tyre_type)                                                                 # проверка совпавших параметров
                    ############################################################################################################################
                            # берем значение из колонки 'объем продаж' ячейка n  и записываем в модель Sales, где tyre= tyre_is     
                            #sale_value = sales_list[row_value_counter]
                            #print(contragent, 'contragen') 
                            ###n = 77 + 1
                            sale_value = n 
                            sales_obj = sales_models.Sales.objects.update_or_create(
                                tyre = obj,
                                #date_of_sales = date.today(),
                                date_of_sales = datetime.date(sell_date),
                                #date_of_sales = datetime.date(2022, 9, 23),
                                #contragent = dictionaries_models.ContragentsModel.objects.all().last(),
                                contragent = dictionaries_models.ContragentsModel.objects.get(contragent_name=contragent),
                                sales_value = int(sale_value),
                                table = sales_table
                            )
                row_value_counter += 1
            ####################################################################################################################################################################
            #for n in dictionaries_models.ContragentsModel.objects.all():
            #    print(n.contragent_name)


            #for a in tyretype_row_dict.values(), model_row_dict.values(), params_row_dict.values():
            #    print(a, len(a))

            #for k, v in tyretype_row_dict.items():
            #    print(k, v, ' k, v')

            ## СОЗДАЕМ БАЗОВУЮ ВАЛЮТУ
            currency_chosen_by_hand = dictionaries_models.Currency.objects.get_or_create(
                currency='BYN'
            )
            ####

            #ik = tyres_models.Tyre.objects.all()
            #for n in ik:
            #    print(n.tyre_size.tyre_size, 'TYRE')

            ######################################                      ВАРИАНТ  2  =  СОПОСТАВЛЕНИЕ СОВПАШИХ ШИН С БД
            #### СОПОСТАВЛЕНИЕ СОВПАШИХ СТРОК С С ШИНАМИ В БД:
            ####
            #tyretype_row_dict, model_row_dict, params_row_dict, saless_row_dict, planned_costs_row_dict, semi_variable_costs_row_dict, belarus902price_costs_row_dict, tpsrussiafcaprice_costs_row, tpskazfcaprice_cost_row, tpsmiddleasiafcaprice_costs_row, tpsmiddleasiafcaprice_costs_row 
            #if len(tyretype_row_dict) == len(model_row_dict) and len(tyretype_row_dict) == len(params_row_dict) and len(tyretype_row_dict) == len(saless_row_dict) and len(tyretype_row_dict) == len(planned_costs_row_dict) and len(tyretype_row_dict) == len(semi_variable_costs_row_dict) and len(tyretype_row_dict) == len(belarus902price_costs_row_dict) and len(tyretype_row_dict) == len(tpsrussiafcaprice_costs_row) and len(tyretype_row_dict) == len(tpskazfcaprice_cost_row) and len(tyretype_row_dict) == len(tpsmiddleasiafcaprice_costs_row):
            #if len(tyretype_row_dict) == len(model_row_dict) and len(tyretype_row_dict) == len(params_row_dict) and len(tyretype_row_dict) == len(planned_costs_row_dict) and len(tyretype_row_dict) == len(semi_variable_costs_row_dict) and len(tyretype_row_dict) == len(belarus902price_costs_row_dict) and len(tyretype_row_dict) == len(tpsrussiafcaprice_costs_row) and len(tyretype_row_dict) == len(tpskazfcaprice_cost_row) and len(tyretype_row_dict) == len(tpsmiddleasiafcaprice_costs_row):
            if len(tyretype_row_dict) == len(model_row_dict) and len(tyretype_row_dict) == len(params_row_dict):
                # выбираем именно по строкам, а не просто по порядку. Ведь  ключ -  номер строки:
                for n in tyretype_row_dict.keys():
                #for n in range(0, len(tyretype_row_dict)):
                    #print(tyretype_row_dict.get(n), 'tyretype_row_dict.get(n)', len(tyretype_row_dict))
                    if tyres_models.Tyre.objects.filter(tyre_model__model=model_row_dict.get(n), tyre_size__tyre_size=tyretype_row_dict.get(n)):
                        #print(model_row_dict.get(n), tyretype_row_dict.get(n), 'tyretype_row_dict.get(n')
                        tyre_mathced_obj = tyres_models.Tyre.objects.filter(tyre_model__model=model_row_dict.get(n), tyre_size__tyre_size=tyretype_row_dict.get(n), tyre_type__tyre_type__in=params_row_dict.get(n))
                        ####for object in tyre_mathced_obj:
                        ####    print(object.tyre_model.model, object.tyre_size.tyre_size,  object.tyre_type.all(), 'n = ', n)
                        for obj in tyre_mathced_obj:              ### берем объекты из кверисета
                            #print(obj.tyre_size.tyre_size, 'tyre_mathced_obj')
                            counter_coinc = 0
                            for param in params_row_dict.get(n):                ### берем параметры перебираем
                                len(params_row_dict.get(n))                     ###  замеряем количество параметров в текущем 
                                dbpar_list = []
                                for p in obj.tyre_type.all():       ###   перебираем параметры в параметрах объекта
                                    if param == p.tyre_type:        ### если параметры совпадают
                                        counter_coinc += 1
                                        #matched = param, '=', p.tyre_type
                                    dbpar_list.append(p.tyre_type)
                            #print('parsed params = ',  params_row_dict.get(n), 'params in DB=', dbpar_list)

                            if counter_coinc == len(params_row_dict.get(n)):        ###### ЗДЕСЬ ПОЛУЧАЕМ ОБЪЕКТ У КОТОРОГО ВСЕ ПАРАМЕТРЫ СОВПАЛИ СПАРАМЕТРАМИ ШИНЫ В БАЗЕ
                                #print('MATCHED!!', obj.tyre_size.tyre_size)

                                sales_ddict = {}
                                sales_ddict['sales_ddict'] = saless_row_dict.get(n)
                                planned_costs_ddict = {}
                                planned_costs_ddict['planned_costs_ddict'] = planned_costs_row_dict.get(n)
                                semi_variable_ddict = {}
                                semi_variable_ddict['semi_variable_ddict'] = semi_variable_costs_row_dict.get(n)
                                belarus902price_costs_ddict = {}
                                belarus902price_costs_ddict['belarus902price_costs_ddict'] = belarus902price_costs_row_dict.get(n)
                                tpsrussiafcaprice_costs_ddict = {}
                                tpsrussiafcaprice_costs_ddict['tpsrussiafcaprice_costs_ddict'] = tpsrussiafcaprice_costs_row.get(n)
                                tpskazfcaprice_cost_ddict = {}
                                tpskazfcaprice_cost_ddict['tpskazfcaprice_cost_ddict'] = tpskazfcaprice_cost_row.get(n)
                                tpsmiddleasiafcaprice_costs_ddict = {}
                                tpsmiddleasiafcaprice_costs_ddict['tpsmiddleasiafcaprice_costs_ddict'] = tpsmiddleasiafcaprice_costs_row.get(n)

                                row_parsing_sales_costs_prices_dict[obj] = sales_ddict, planned_costs_ddict, semi_variable_ddict, belarus902price_costs_ddict, tpsrussiafcaprice_costs_ddict, tpskazfcaprice_cost_ddict, tpsmiddleasiafcaprice_costs_ddict, n 
                #print('JJJJJJJJJJJJ', current_prices_row, 'current_prices_row')

                current_prices_ddict = {}
                for n in range(0, len(current_prices_row)):
                    #print(current_prices_row.get(n))
                    if tyres_models.Tyre.objects.filter(tyre_model__model=model_row_dict.get(n), tyre_size__tyre_size=tyretype_row_dict.get(n)):
                        tyre_mathced_obj = tyres_models.Tyre.objects.filter(tyre_model__model=model_row_dict.get(n), tyre_size__tyre_size=tyretype_row_dict.get(n), tyre_type__tyre_type__in=params_row_dict.get(n))
                        ####for object in tyre_mathced_obj:
                        ####    print(object.tyre_model.model, object.tyre_size.tyre_size,  object.tyre_type.all(), 'n = ', n)
                        for obj in tyre_mathced_obj:              ### берем объекты из кверисета
                            counter_coinc = 0
                            for param in params_row_dict.get(n):                ### берем параметры перебираем
                                len(params_row_dict.get(n))                     ###  замеряем количество параметров в текущем 
                                dbpar_list = []
                                for p in obj.tyre_type.all():       ###   перебираем параметры в параметрах объекта
                                    if param == p.tyre_type:        ### если параметры совпадают
                                        counter_coinc += 1
                                        #matched = param, '=', p.tyre_type
                                    dbpar_list.append(p.tyre_type)
                            #print('parsed params = ',  current_prices_row.get(n), 'params in DB=', dbpar_list)

                            
                            if counter_coinc == len(params_row_dict.get(n)):        ###### ЗДЕСЬ ПОЛУЧАЕМ ОБЪЕКТ У КОТОРОГО ВСЕ ПАРАМЕТРЫ СОВПАЛИ СПАРАМЕТРАМИ ШИНЫ В БАЗЕ
                                #print('MATCHED!!', obj)
                                
                                #current_prices_ddict['tpsmiddleasiafcaprice_costs_ddict'] = current_prices_row.get(n)
                                current_prices_ddict[obj] = current_prices_row.get(n)


                #print('current_prices_ddict', current_prices_ddict)
            #for key, value in row_parsing_sales_costs_prices_dict.items():
            #    print(key.tyre_size.tyre_size, 'row_parsing_sales_costs_prices_dict', value)  
            ##############          КЛЮЧЕВАЯ ШТУКА:         !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #print('row_parsing_sales_costs_prices_dict', row_parsing_sales_costs_prices_dict)           #### !!!!!!!!!!! КОНТРОЛЬНЫЙ СЛОВАРЬ СО СВОДОМ ПОСТРОЧНЫМ СОВПАШИХ С БД ШИН И СПАРСЕННЫМИ ДАННЫМИ как аналог list_of_unique_tyres_objs_cleaned n = номер строки!!!
            #Tyre object (1059) ({'sales_ddict': None}, {'planned_costs_ddict': 27541}, {'semi_variable_ddict': 18935}, {'belarus902price_costs_ddict': 33321}, {'tpsrussiafcaprice_costs_ddict': 37245}, {'tpskazfcaprice_cost_ddict': 37226}, {'tpsmiddleasiafcaprice_costs_ddict': 48877}, 25)
            #'row_parsing_sales_costs_prices_dict':
            # [0]['sales_ddict']                        # объем продаж
            # [1]['planned_costs_ddict']                # себестоимость
            # [2]['semi_variable_ddict']                # плановые затраты
            # [3]['belarus902price_costs_ddict']        # 902,9 РБ
            # [4]['tpsrussiafcaprice_costs_ddict']      # ТПС РФ
            # [5]['tpskazfcaprice_cost_ddict']          # ТПС Казахстан
            # [6]['tpsmiddleasiafcaprice_costs_ddict']  # ТПС Азия
            ####### [7]['current_prices_ddict']               # действующие цены
            # [8] = номер строки                        # номер строки из спарсингованной таблицы
            #########
            #'current_prices_ddict'                     # действующие цены - отдельный словарь

            for k, v in row_parsing_sales_costs_prices_dict.items():       # ПРЕДПРОСМОТР СПИСКА СОВПАВШИХ ШИН И ДАННЫХ
                parrams = []
                for par in k.tyre_type.all():
                    parrams.append(par.tyre_type)
                print(k.tyre_size.tyre_size, k.tyre_model.model, parrams, v)

            # ЗАБРАСЫВАЕМ ПОЛНЫЕ ЗАТРАТЫ:
            for key, obj_list_el in row_parsing_sales_costs_prices_dict.items():
                #print(obj_list_el[1]['planned_costs_ddict'] , 'KKK')
                if obj_list_el[1]['planned_costs_ddict']:
                        planned_costs_object = prices_models.PlannedCosstModel.objects.update_or_create(
                            tyre = key,     
                            price = obj_list_el[1]['planned_costs_ddict'],
                            #date_period = date_from_table,                 # ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ
                            date_period = datetime.now(),   
                            currency = currency_chosen_by_hand[0]         
                        )

            # ЗАБРАСЫВАЕМ ПЛАНОВУЮ СЕБЕСТОИМОСТЬ:
            for key, obj_list_el in row_parsing_sales_costs_prices_dict.items():
                if obj_list_el[2]['semi_variable_ddict']:
                        semi_variable_costs_object = prices_models.SemiVariableCosstModel.objects.update_or_create(
                            tyre = key,     
                            price = obj_list_el[2]['semi_variable_ddict'],
                            #date_period = date_from_table,                 # ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ
                            date_period = datetime.now(),   
                            currency = currency_chosen_by_hand[0]         
                        )

            # ЗАБРАСЫВАЕМ прейскуранты №№9, 902:
            for key, obj_list_el in row_parsing_sales_costs_prices_dict.items():
                if obj_list_el[3]['belarus902price_costs_ddict']:
                        belarus902price_costs_object = prices_models.Belarus902PriceModel.objects.update_or_create(
                            tyre = key,     
                            price = obj_list_el[3]['belarus902price_costs_ddict'],
                            #date_period = date_from_table,                 # ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ
                            date_period = datetime.now(),   
                            currency = currency_chosen_by_hand[0]         
                        )

            # ЗАБРАСЫВАЕМ даннын по  ТПС РФ FCA:
            for key, obj_list_el in row_parsing_sales_costs_prices_dict.items():
                if obj_list_el[4]['tpsrussiafcaprice_costs_ddict']:
                        tpsrussiafcaprice_object = prices_models.TPSRussiaFCAModel.objects.update_or_create(
                            tyre = key,     
                            price = obj_list_el[4]['tpsrussiafcaprice_costs_ddict'],
                            #date_period = date_from_table,                 # ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ
                            date_period = datetime.now(),   
                            currency = currency_chosen_by_hand[0]         
                        )
            
            # ЗАБРАСЫВАЕМ даннын по ТПС Казахстан FCA:
            for key, obj_list_el in row_parsing_sales_costs_prices_dict.items():
                if obj_list_el[5]['tpskazfcaprice_cost_ddict']:
                        tpskazfcaprice_object = prices_models.TPSKazFCAModel.objects.update_or_create(
                            tyre = key,     
                            price = obj_list_el[5]['tpskazfcaprice_cost_ddict'],
                            #date_period = date_from_table,                 # ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ
                            date_period = datetime.now(),   
                            currency = currency_chosen_by_hand[0]         
                        )

            # ЗАБРАСЫВАЕМ даннын по ТПС Средняя Азия, Закавказье, Молдова FCA:
            for key, obj_list_el in row_parsing_sales_costs_prices_dict.items():
                if obj_list_el[6]['tpsmiddleasiafcaprice_costs_ddict']:
                        tpsmiddleasiafcaprice_object = prices_models.TPSMiddleAsiaFCAModel.objects.update_or_create(
                            tyre = key,     
                            price = obj_list_el[6]['tpsmiddleasiafcaprice_costs_ddict'],
                            #date_period = date_from_table,                 # ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ
                            date_period = datetime.now(),   
                            currency = currency_chosen_by_hand[0]         
                        )

            #print(row_parsing_sales_costs_prices_dict.items(), 'row_parsing_sales_costs_prices_dict.items()')
            # ЗАБРАСЫВАЕМ даннын по Действующие цены:
            #for key, obj_list_el in row_parsing_sales_costs_prices_dict.items():
            for key, obj_list_el in current_prices_ddict.items():
                #print('row_parsing_sales_costs_prices_dict', key, obj_list_el )             #current_prices_ddict['tpsmiddleasiafcaprice_costs_ddict']
                if obj_list_el:
                        currentpricesprice_object = prices_models.CurrentPricesModel.objects.update_or_create(
                            tyre = key,     
                            price = obj_list_el,
                            #date_period = date_from_table,                 # ЗДЕСЬ ПРОПИСЫВАТЬ ДАТУ ВМЕСТО ЗАГЛУШКИ
                            date_period = datetime.now(),   
                            currency = currency_chosen_by_hand[0]         
                        )

        # Создаем справочники по базовым валютам:
        base_currencies = ['RUB', 'BYN', 'USD', 'EURO']
        for curr in base_currencies:
            dictionaries_models.Currency.objects.get_or_create(
                currency = curr
            )
        ###

        ## соберем Tyre_Sale объекты:
        for obj in tyres_models.Tyre.objects.all():
            tyr_sal = sales_models.Tyre_Sale.objects.update_or_create(
                tyre = obj,
                table = sales_table
            )

        #### соберем объекты ABC из шин и объектов Sales:

        #0) создадим объект таблицы AbcxyzTable для проверки:
        table_id = self.request.session.get('table_id')             
        abc_table_get = abc_table_xyz_models.AbcxyzTable.objects.filter(pk=table_id)
        if abc_table_get:
            abc_table = abc_table_get[0]
        else:
            abc_table_queryset = abc_table_xyz_models.AbcxyzTable.objects.update_or_create()
            abc_table = abc_table_queryset[0]
        # 1) возмем все объекты шин:
        for obj in tyres_models.Tyre.objects.all():
            tyre_obj = obj
        # 2) возмем все объекты продаж:
            sales_obj_set = sales_models.Sales.objects.filter(tyre=tyre_obj)
            #print(sales__obj_set)       # <QuerySet [<Sales: Sales object (999)>, <Sales: Sales object (1017)>]>
            #print(list(sales__obj_set))
        # 3) создадим объекты модели Abcxyz
            abc_obj = abc_table_xyz_models.Abcxyz.objects.filter(table=abc_table, tyre=tyre_obj)
            abc_obj_set = abc_table_xyz_models.Abcxyz.objects.update_or_create(
                table=abc_table,
                tyre=tyre_obj,
            )
            for sales_obj in sales_obj_set:
                abc_obj_set[0].sales.add(sales_obj)
            #print(abc_obj_set[0].sales.all(), 'JJJJJJJJ')

        #####if abc_table:
        #####    #print(abc_table, '==', abc_table.tyre_total, abc_table.list_of_total_sales_of_of_tyre_in_period())
        #####    pass
        #for obj in abc_table_xyz_models.Abcxyz.objects.all():
        #    #print(obj.total_sales_of_of_tyre_in_period(), obj.percent_in_total_amount())
        #    print(obj.abc_group[0])

        #0) создадим объект таблицы ComparativeAnalysisTableModel для проверки:

        table_id = self.request.session.get('table_id')             
        comparative_analysis_table_get = prices_models.ComparativeAnalysisTableModel.objects.filter(pk=table_id)
        if comparative_analysis_table_get:
            comparative_analysis_table = comparative_analysis_table_get[0]
        else:
            comparative_analysis_table_queryset = prices_models.ComparativeAnalysisTableModel.objects.update_or_create()
            comparative_analysis_table = comparative_analysis_table_queryset[0]

        # 1) возмем все объекты шин:
        for key in row_parsing_sales_costs_prices_dict.keys():
            tyre_obj = key
        # 2.1) возмем все объекты плановой себестоимости:
            planned_costs_obj_set = prices_models.PlannedCosstModel.objects.filter(tyre=tyre_obj)            # !!!! ФИЛЬТР ВСЕХ ОБЪЕКТОВ + ДОБАВИТЬ ФИЛЬТР ПО ПЕРИОДУ   ===== date_period
            #planned_costs_obj_set = prices_models.PlannedCosstModel.objects.get(tyre=tyre_obj)                  # ОДИН объект на дату + ДОБАВИТЬ ФИЛЬТР ПО ПЕРИОДУ   ===== date_period
            if planned_costs_obj_set:
                planned_costs_obj_set = planned_costs_obj_set[0]
            else:       # если пустой кверисет
                planned_costs_obj_set = None
        # 2.2) возмем все объекты прямые затраты:
            semi_variable_costs_obj_set = prices_models.SemiVariableCosstModel.objects.filter(tyre=tyre_obj)
            #semi_variable_costs_obj_set = prices_models.SemiVariableCosstModel.objects.get(tyre=tyre_obj)
            if semi_variable_costs_obj_set:
                semi_variable_costs_obj_set = semi_variable_costs_obj_set[0]
            else:       # если пустой кверисет
                semi_variable_costs_obj_set = None
        # 2.3) возмем все объекты прейскуранты №№9, 902:
            belarus902price_obj_set = prices_models.Belarus902PriceModel.objects.filter(tyre=tyre_obj)
            #belarus902price_obj_set = prices_models.Belarus902PriceModel.objects.get(tyre=tyre_obj)
            if belarus902price_obj_set:
                belarus902price_obj_set = belarus902price_obj_set[0]
                #print('belarus902price_obj_set', belarus902price_obj_set.price)
            else:       # если пустой кверисет
                belarus902price_obj_set = None
        # 2.4) возмем все объекты прейскуранты ТПС РФ FCA:
            tpsrussiafcaprice_obj_set = prices_models.TPSRussiaFCAModel.objects.filter(tyre=tyre_obj)
            #tpsrussiafcaprice_obj_set = prices_models.TPSRussiaFCAModel.objects.get(tyre=tyre_obj)
            if  tpsrussiafcaprice_obj_set:
                tpsrussiafcaprice_obj_set = tpsrussiafcaprice_obj_set[0]
            else:       # если пустой кверисет
                tpsrussiafcaprice_obj_set = None
        # 2.5) возмем все объекты прейскуранты ТПС Казахстан FCA:
            tpskazfcaprice_obj_set = prices_models.TPSKazFCAModel.objects.filter(tyre=tyre_obj)
            #tpskazfcaprice_obj_set = prices_models.TPSKazFCAModel.objects.get(tyre=tyre_obj)
            if  tpskazfcaprice_obj_set:
                tpskazfcaprice_obj_set = tpskazfcaprice_obj_set[0]
            else:       # если пустой кверисет
                tpskazfcaprice_obj_set = None
        # 2.6) возмем все объекты прейскуранты ТПС Средняя Азия, Закавказье, Молдова FCA:
            tpsmiddleasiafcaprice_obj_set = prices_models.TPSMiddleAsiaFCAModel.objects.filter(tyre=tyre_obj)
            #tpsmiddleasiafcaprice_obj_set = prices_models.TPSMiddleAsiaFCAModel.objects.get(tyre=tyre_obj)
            if tpsmiddleasiafcaprice_obj_set:
                tpsmiddleasiafcaprice_obj_set = tpsmiddleasiafcaprice_obj_set[0]
            else:       # если пустой кверисет
                tpsmiddleasiafcaprice_obj_set = None
        # 2.7) возмем все объекты Действующие цены:
            currentpricesprice_obj_set = prices_models.CurrentPricesModel.objects.filter(tyre=tyre_obj)
            #currentpricesprice_obj_set = prices_models.CurrentPricesModel.objects.get(tyre=tyre_obj)
            if currentpricesprice_obj_set:
                currentpricesprice_obj_set = currentpricesprice_obj_set[0]
            else:       # если пустой кверисет
                currentpricesprice_obj_set = None
            #print(planned_costs_obj_set.price, semi_variable_costs_obj_set.price, belarus902price_obj_set.price, 'HHH')


        # 3) создадим объекты модели ComparativeAnalysisTyresModel

            #defaults = dict(
            #    planned_costs=planned_costs.price,
            #    semi_variable_prices=semi_variable_prices,
            #    belarus902price=belarus902price,
            #    tpsrussiafcaprice=0,
            #    tpskazfcaprice=0,
            #    tpsmiddleasiafcaprice=0,
            #    currentpricesprice=0,                
            #)

            comparative_analysis_tyres_obj_set = prices_models.ComparativeAnalysisTyresModel.objects.update_or_create(
                table=comparative_analysis_table,
                tyre=tyre_obj,
                planned_costs=planned_costs_obj_set,
                semi_variable_prices=semi_variable_costs_obj_set,
                belarus902price=belarus902price_obj_set,
                tpsrussiafcaprice=tpsrussiafcaprice_obj_set,
                tpskazfcaprice=tpskazfcaprice_obj_set,
                tpsmiddleasiafcaprice=tpsmiddleasiafcaprice_obj_set,
                currentpricesprice=currentpricesprice_obj_set,
                #defaults={'semi_variable_prices': 0, 'belarus902price': 0, 'tpsrussiafcaprice': 0, 'tpskazfcaprice': 0, 'tpsmiddleasiafcaprice': 0, 'currentpricesprice': 0, 'currentpricesprice': 0},
                )

        #row_value = 0
        #for j in prices_models.ComparativeAnalysisTyresModel.objects.all():
        #    if j.planned_costs is None:
        #        pass
        #    else:
        #        print(j.planned_costs.price, 'JJJJJJJ', row_value)
        #    row_value += 1


        ############################################ Запись данных в существующий файл в столбец:
        from openpyxl import load_workbook
        excel_file = load_workbook('Tyres.xlsx')
        excel_sheet = excel_file["Holidays 2019"]
        #print(excel_file.sheetnames, 'TTTTTTTTTTTTTTTTTT')

        ###### получить количество объектов Sales:
        row_value = 0
        for ob_val in sales_models.Sales.objects.all():
            row_value += 1
        
        #генератор для хождения по строкам:    
        def raw_generator(n, stop):
            while True:
                if n > stop:
                    raise StopIteration
                yield n
                n += 1
        max_raw = row_value     
        i = 2       # со второй строки        
        row_curr = raw_generator(i, max_raw+i)

        for sales_obj in sales_models.Sales.objects.all():
            val = next(row_curr)
            excel_sheet['E1'] = 'Tyre Size'
            excel_sheet.cell(row=val, column=5).value = sales_obj.tyre.tyre_size.tyre_size

            excel_sheet['F1'] = 'Model'
            excel_sheet.cell(row=val, column=6).value = sales_obj.tyre.tyre_model.model

            excel_sheet['G1'] = 'Param'
            str_obj_param_list = []
            str_obj_param_str = ''
            for type_obj in sales_obj.tyre.tyre_type.all():
                str_obj_param_list.append(type_obj.tyre_type)
            str_obj_param_str = ', '.join(str_obj_param_list)
            #print(str_obj_param_str)
            excel_sheet.cell(row=val, column=7).value = str_obj_param_str

            excel_sheet['H1'] = 'Sales value'
            excel_sheet.cell(row=val, column=8).value = sales_obj.sales_value

            excel_sheet['I1'] = 'Date_of_sales'
            excel_sheet.cell(row=val, column=9).value = sales_obj.date_of_sales

            excel_sheet['J1'] = 'Contragent'
            excel_sheet.cell(row=val, column=10).value = sales_obj.contragent.contragent_name

            excel_file.save(filename="Tyres.xlsx")                                 
        form = forms.ImportSalesDataForm()
        #################################################                
        return render(self.request, 'filemanagment/excel_import.html', {'form': form}) 

