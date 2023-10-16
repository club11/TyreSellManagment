from dataclasses import field, fields
from django import forms
from prices import models as prices_models
from . import models as chemcurier_models
import pandas as pd

INITIAL_PERIOD = None
PERIODS = None

INITIAL_TYREISIZE = None
TYRESIZES = None

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
    print('list_of_choices!!!!!!', list_of_choices)
    return list_of_choices

def get_tyresizes_list():
    list_of_tyresizes = []
    list_of_tyresizes_only = []
    for obj in prices_models.ChemCurierTyresModel.objects.all():
        list_of_tyresizes_only.append(obj.tyre_size_chem)
    list_of_tyresizes_only = list(set(list_of_tyresizes_only))  
    print('get_tyresizes!!', list_of_tyresizes_only)
    for trsz in list_of_tyresizes_only:      # добавляем ключи:
        resizes_k_and_val = trsz, trsz
        list_of_tyresizes.append(resizes_k_and_val)
    return list_of_tyresizes



PERIODS = get_chem_periods() 
TYRESIZES = get_tyresizes_list()


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