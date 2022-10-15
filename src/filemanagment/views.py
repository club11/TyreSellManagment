from asyncio.windows_events import NULL
import datetime
from enum import unique
from operator import index
from turtle import st
from unicodedata import decimal, name
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
        contragent_list = []            #контрагент
        column_sell_date = ''           #строка с датой продажи
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
        ################ считывание файла и сопоставление с текущей базой данных:
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


                        if cell.value == 'дата':        # получаем строку'дата'
                            #print(cell.value)    
                            #print(cell.coordinate) 
                            cell = sheet.cell(row=cell.row+1, column=cell.column)
                            column_sell_date = cell.value
                        elif cell.value == 'объем продаж':
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
                                    pass
                            sales_list = [float(x) for x in sales_list]    # str значения в float
                                                # 1 Парсинг
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

                #print(tyresize_list, len(tyresize_list))           
                #print(tyremodel_list, len(tyremodel_list))
                #print(tyreparametrs_list, len(tyreparametrs_list))  

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
            #print(len(tyreparam_list_with_lists), tyreparam_list_with_lists)    # 3/2  в виде списка с вложенными списками

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
                    #    print('YEAP!', tyre_obj_exist)
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
                #if contragent_list:
                #    contragent = contragent_list.pop(0)
                #    #contragent_name = 'БНХ РОС'
                #    if contragent:
                #        dictionaries_models.ContragentsModel.objects.get_or_create(
                #            contragent_name = contragent
                #            )
                #    if contragent is None:
                #        contragent = ''
                #        dictionaries_models.ContragentsModel.objects.get_or_create(
                #            contragent_name = contragent
                #            )      
                #    else:
                #        contragent = ''
                #        dictionaries_models.ContragentsModel.objects.get_or_create(
                #            contragent_name = contragent
                #            )
                #else:
                #    contragent = ''
                #    dictionaries_models.ContragentsModel.objects.get_or_create(
                #        contragent_name = contragent
                #        )  
                dictionaries_models.ContragentsModel.objects.get_or_create(
                    contragent_name = 'БНХ РОС'
                    )                             

                for obj in obj_list_el:
                #    ############################################################################################################################
                #    print(obj.tyre_model.model, obj.tyre_size.tyre_size)       # проверка совпавших параметров
                #    course_qs = obj.tyre_type.all()                                                         # проверка совпавших параметров
                #    for course in course_qs:                                                                    # проверка совпавших параметров
                #        print(course.tyre_type)                                                                 # проверка совпавших параметров
                    ############################################################################################################################
                            # берем значение из колонки 'объем продаж' ячейка n  и записываем в модель Sales, где tyre= tyre_is     
                            #sale_value = sales_list[row_value_counter]
                            ###n = 77 + 1
                            sale_value = n 
                            sales_obj = sales_models.Sales.objects.update_or_create(
                                tyre = obj,
                                #date_of_sales = date.today(),
                                date_of_sales = datetime.date(sell_date),
                                #date_of_sales = datetime.date(2022, 9, 23),
                                contragent = dictionaries_models.ContragentsModel.objects.all().last(),
                                #contragent = dictionaries_models.ContragentsModel.objects.get(contragent_name=contragent),
                                sales_value = int(sale_value),
                                table = sales_table
                            )
                row_value_counter += 1
            ####################################################################################################################################################################
            for n in dictionaries_models.ContragentsModel.objects.all():
                print(n.contragent_name)

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
                tyre = tyre_obj,
            )
            for sales_obj in sales_obj_set:
                abc_obj_set[0].sales.add(sales_obj)
            #print(abc_obj_set[0].sales.all(), 'JJJJJJJJ')


        #####if abc_table:
        #####    #print(abc_table, '==', abc_table.tyre_total, abc_table.list_of_total_sales_of_of_tyre_in_period())
        #####    pass
        #####

        #for obj in abc_table_xyz_models.Abcxyz.objects.all():
        #    #print(obj.total_sales_of_of_tyre_in_period(), obj.percent_in_total_amount())
        #    print(obj.abc_group[0])

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

