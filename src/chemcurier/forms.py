from dataclasses import field, fields
from django import forms
from prices import models as prices_models
from . import models as chemcurier_models
import pandas as pd

INITIAL_PERIOD = None
PERIODS = None

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

def get_chem_periods():
    earlest_date = prices_models.ChemCurierTyresModel.objects.earliest('data_month_chem').data_month_chem
    latestst_date = prices_models.ChemCurierTyresModel.objects.latest('data_month_chem').data_month_chem
    period_of_dates_chem_in_base = pd.date_range(earlest_date, latestst_date, freq='MS').date
    list_of_choices = []
    for dattte in period_of_dates_chem_in_base:
        str_date = dattte.strftime('%m.%Y')
        str_date_and_date = dattte, str_date
        list_of_choices.append(str_date_and_date)
    list_of_choices = list(reversed(list_of_choices))
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
    return list_of_groups  


PERIODS = get_chem_periods() 
TYRESIZES = get_tyresizes_list()
BRANDS = get_tyrebrands_list()
RECIEVERS = get_recievers_list()
PRODCOUTRYS = get_prod_countrys_list()
GROUPS = get_groups_list()

class PeriodForm(forms.Form): 
    Parameter_CHOICES = PERIODS   
    periods = forms.ChoiceField(
        widget = forms.Select,
        choices = Parameter_CHOICES,
        label='Период',      
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
        label='Стана производства',   
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