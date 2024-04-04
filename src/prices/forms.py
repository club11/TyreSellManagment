from dataclasses import field, fields
from django import forms
from dictionaries import models
from . import models as prices_models
from django.core.exceptions import ValidationError
import datetime
from homepage.templatetags import my_tags
from . import views as prices_views
from validators.validators import competitor_num_validator



#class FilterForm(forms.Form):
#    competitors = forms.ModelMultipleChoiceField(
#        queryset = models.CompetitorModel.objects.filter(developer_competitor__site__in=['onliner.by', 'bagoria.by', 'autoset.by']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'), 
#    #    widget = forms.CheckboxSelectMultiple(attrs={"checked":""}),                                                                                            ### initial не работает, пришлось тупо влесть в queryset. тупо аж капец                                        #####
#        widget = forms.CheckboxSelectMultiple(), 
#    )

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    a = self.fields['competitors'].choices
    #    b = self.__iter__()
    #    print('a', a)
    #    print('b', b)


#class FilterForm(forms.Form):
#    competitors = forms.MultipleChoiceField(
#    label=u"Select multiple", 
#    choices=MY_CHOICES, 
#    widget=forms.widgets.CheckboxSelectMultiple, 
#    initial=(c[0] for c in MY_CHOICES)
#)


class FilterRussiaForm(forms.Form):
    competitors = forms.ModelMultipleChoiceField(
        queryset = models.CompetitorModel.objects.filter(developer_competitor__site__in=['express-shina.ru', 'kolesatyt.ru', 'kolesa-darom.ru']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'), 
        widget = forms.CheckboxSelectMultiple(),                                                                                            ### initial не работает, пришлось тупо влесть в queryset. тупо аж капец                                        #####
    )

class DeflectionInputForm(forms.Form):
    deflection_data = forms.FloatField(required=None, max_value=100, min_value=0, 
    #widget=forms.NumberInput(attrs={'id': 'deflection_data', 'step': "0.01"}), label='торг. надбавка, (%)',)
    widget=forms.NumberInput(attrs={'id': 'deflection_data', 'step': "0.01"}), label='')

class PaginationInputForm(forms.Form):
    pagination_data = forms.IntegerField(required=None, max_value=25, min_value=0, 
    #widget=forms.NumberInput(attrs={'id': 'pagination_data', 'step': "1"}), label='кол-во позиций в таблице (1-25)')
    widget=forms.NumberInput(attrs={'id': 'pagination_data', 'step': "1"}), label='')

class CompetitoPerSiteInputForm(forms.Form):
    competitor_pagination_data = forms.IntegerField(required=True, max_value=5, min_value=1, 
    #widget=forms.NumberInput(attrs={'id': 'competitor_pagination_data', 'step': "1"}), label='кол-во конкурентов в таблице (0-5)')
    widget=forms.NumberInput(attrs={'id': 'competitor_pagination_data', 'step': "1"}), label='')

class CurrencyDateInputForm(forms.Form):
    #chosen_date_for_currency = forms.DateField(widget=forms.DateInput(format='%m-%Y-%d'))
    chosen_date_for_currency = forms.DateField(widget=forms.SelectDateWidget(years=range(2022,2024)),
    #label='курс НБ РБ на:',
    label='',
    initial='2022-7-7'

    )

    
    #initial=datetime.date.today())  
    
    

