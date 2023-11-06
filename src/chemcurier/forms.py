from dataclasses import field, fields
from django import forms
from prices import models as prices_models
from . import models as chemcurier_models
import pandas as pd

PERIODS_IN_STR_MONTH_TEMPORARY = []
PERIODS_IN_STR_MONTH = []
PERIODS_IN_STR_YEARS = []

INITIAL_PERIOD = None
PERIODS = None
INITIAL_PERIOD_START = None
INITIAL_PERIOD_END = None

INITIAL_TYREISIZE = None
TYRESIZES = None

INITIAL_BRANDS = None
BRANDS = None

INITIAL_RECIEVER = None
RECIEVERS = None 

INITIAL_PRODCOUTRYS = None
PRODCOUTRYS = None

INITIAL_GROUPS = None
GROUPS = None

CHEMCOURIER_EXCEL_CREATE = False
CHEMCOURIER_PROGRESSIVE_EXCEL_CREATE = False

def get_chem_periods():
    list_of_choices = []
    try:
        earlest_date = prices_models.ChemCurierTyresModel.objects.earliest('data_month_chem').data_month_chem
        latestst_date = prices_models.ChemCurierTyresModel.objects.latest('data_month_chem').data_month_chem
        period_of_dates_chem_in_base = pd.date_range(earlest_date, latestst_date, freq='MS').date

        for dattte in period_of_dates_chem_in_base:
            str_date = dattte.strftime('%m.%Y')
            str_date_and_date = dattte, str_date
            list_of_choices.append(str_date_and_date)
        list_of_choices = list(reversed(list_of_choices))
    except:
        pass
    #print('list_of_choices', list_of_choices)
    return list_of_choices

def get_tyresizes_list():
    list_of_tyresizes = []
    list_of_tyresizes_only = []
    for obj in prices_models.ChemCurierTyresModel.objects.all():
        list_of_tyresizes_only.append(obj.tyre_size_chem)
    list_of_tyresizes_only = list(set(list_of_tyresizes_only))  
    for trsz in list_of_tyresizes_only:      # добавляем ключи:
        resizes_k_and_val = trsz, trsz
        list_of_tyresizes.append(resizes_k_and_val)
    print('list_of_tyresizes === ')
    list_of_tyresizes.sort()
    return list_of_tyresizes

def get_tyrebrands_list():
    list_of_tyrebrandss = [('-','-')]
    list_of_tyrebrands_only = [] 
    for obj in prices_models.ChemCurierTyresModel.objects.all():
      list_of_tyrebrands_only.append(obj.producer_chem)  
    list_of_tyrebrands_only = list(set(list_of_tyrebrands_only))
    for brnd in list_of_tyrebrands_only:      # добавляем ключи:
        tyrebrands_val = brnd, brnd
        list_of_tyrebrandss.append(tyrebrands_val)
    list_of_tyrebrandss.sort()      
    return list_of_tyrebrandss  

def get_recievers_list():
    list_of_recievers = [('-','-')]
    list_of_recievers_only = [] 
    for obj in prices_models.ChemCurierTyresModel.objects.all():
      list_of_recievers_only.append(obj.reciever_chem)  
    list_of_recievers_only = list(set(list_of_recievers_only))
    for reciever_chem in list_of_recievers_only:      # добавляем ключи:
        recievers_val = reciever_chem, reciever_chem
        list_of_recievers.append(recievers_val)
    list_of_recievers.sort()
    return list_of_recievers  

def get_prod_countrys_list():
    list_of_prod_country = [('-','-')]
    list_of_prod_country_only = [] 
    for obj in prices_models.ChemCurierTyresModel.objects.all():
      list_of_prod_country_only.append(obj.prod_country)  
    list_of_prod_country_only = list(set(list_of_prod_country_only))
    for prod_country in list_of_prod_country_only:      # добавляем ключи:
        prod_country_val = prod_country, prod_country
        list_of_prod_country.append(prod_country_val)
    list_of_prod_country.sort()    
    return list_of_prod_country  

def get_groups_list():
    list_of_groups = [('-','-')]
    list_of_groups_only = [] 
    for obj in prices_models.ChemCurierTyresModel.objects.all():
      list_of_groups_only.append(obj.group_chem)  
    list_of_groups_only = list(set(list_of_groups_only))
    for group_chem in list_of_groups_only:      # добавляем ключи:
        group_chem_val = group_chem.tyre_group, group_chem.tyre_group
        list_of_groups.append(group_chem_val)
    list_of_groups.sort()
    return list_of_groups  

NUMBER_TO_MONTH_DICT = { 1 : 'январь', 2: 'февраль', 3 : 'март', 4 : 'апрель', 5 : 'май', 6 :'июнь', 7 : 'июль', 8 : 'август', 9 : 'сентябрь', 10 : 'октябрь', 11 : 'ноябрь', 12 : 'декабрь'}
MONTH_TO_NUMBER_DICT = { 'январь' : 1, 'февраль': 2, 'март' : 3, 'апрель' : 4, 'май' : 5, 'июнь' : 6, 'июль' : 7, 'август' : 8, 'сентябрь' : 9, 'октябрь' : 10, 'ноябрь' : 11, 'декабрь' : 12}

PERIODS = get_chem_periods() 
TYRESIZES = get_tyresizes_list()
BRANDS = get_tyrebrands_list()
RECIEVERS = get_recievers_list()
PRODCOUTRYS = get_prod_countrys_list()
GROUPS = get_groups_list()

#print('PERIODS', PERIODS)


for name_period in NUMBER_TO_MONTH_DICT.keys():
    if PERIODS:
        for date_period in PERIODS:
            date_period_month, date_period_year = date_period[1].split('.')
            date_period_month_int = int(date_period_month)
            #print('date_period_month', date_period_month, type(date_period_month), 'name_period', name_period, type(name_period))
            if date_period_month_int == name_period:
                #print('AVD', NUMBER_TO_MONTH_DICT.get(name_period))
                month_in_str = NUMBER_TO_MONTH_DICT.get(name_period) 
                year_in_str = date_period_year
                #month_in_str_data = date_period[0], month_in_str
                #year_in_str_data = date_period[0], year_in_str
                #PERIODS_IN_STR_MONTH.append(month_in_str_data)
                #PERIODS_IN_STR_YEARS.append(year_in_str_data)

                month_year_in_str = date_period[0], month_in_str + ' '+ year_in_str                                
                PERIODS_IN_STR_MONTH_TEMPORARY.append(month_year_in_str)

#PERIODS_IN_STR_MONTH = list(set(PERIODS_IN_STR_MONTH))
#PERIODS_IN_STR_YEARS = list(set(PERIODS_IN_STR_YEARS))
#print('PERIODS_IN_STR_MONTH ', PERIODS_IN_STR_MONTH)
#print('PERIODS_IN_STR_YEARS ', PERIODS_IN_STR_YEARS)
PERIODS = list(reversed(PERIODS_IN_STR_MONTH_TEMPORARY))
#print('PERIODS', PERIODS)

class PeriodForm(forms.Form): 
    Parameter_CHOICES = PERIODS 
    periods = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES,
        label='Период',      
    )    
    #periods_month = forms.ChoiceField(
    #    widget = forms.Select,
    #    choices = Parameter_CHOICES,
    #    label='Период',      
    #)
    #Parameter_CHOICES = PERIODS_IN_STR_YEARS  
    #periods_years = forms.ChoiceField(
    #    widget = forms.Select,
    #    choices = Parameter_CHOICES,
    #    label='Период',      
    #)

class StartPeriodForm(forms.Form): 
    Parameter_CHOICES = PERIODS 
    periods_start = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES,
        label='Период начальный',      
    )  

class EndPeriodForm(forms.Form): 
    Parameter_CHOICES = PERIODS 
    periods_end = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES,
        label='Период конечный',      
    )  

class TyreSizeForm(forms.Form): 
    Parameter_CHOICES_TYRESIZES = TYRESIZES   
    tyresizes = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES_TYRESIZES,
        label='Типоразмер',     
    )

class BrandForm(forms.Form): 
    Parameter_CHOICES_BRANDS = BRANDS  
    tyrebrands = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES_BRANDS,
        label='Бренд',   
        required=False,  
    )
    

class RecieverForm(forms.Form): 
    Parameter_CHOICES_RECIEVERS = RECIEVERS  
    recievers = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES_RECIEVERS,
        label='Получатель',   
        required=False,  
    )

class ProdCountryForm(forms.Form): 
    Parameter_CHOICES_PRODCOUTRYS = PRODCOUTRYS  
    prod_countrys = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES_PRODCOUTRYS,
        label='Страна производства',   
        required=False,  
    )

class GroupForm(forms.Form): 
    Parameter_CHOICES_GROUPS = GROUPS  
    prod_groups = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES_GROUPS,
        label='Группа шин',   
        required=False,  
    )



