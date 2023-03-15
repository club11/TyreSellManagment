from dataclasses import field, fields
from django import forms
from dictionaries import models
from . import models as prices_models
from django.core.exceptions import ValidationError
import datetime
from homepage.templatetags import my_tags
from . import views as prices_views
from validators.validators import competitor_num_validator


class FilterForm(forms.Form):
    competitors = forms.ModelMultipleChoiceField(
        queryset = models.CompetitorModel.objects.filter(developer_competitor__site__in=['onliner.by', 'bagoria.by', 'autoset.by']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'), 
        widget = forms.CheckboxSelectMultiple(),                                                                                            ### initial не работает, пришлось тупо влесть в queryset. тупо аж капец                                        #####
    )

class FilterRussiaForm(forms.Form):
    competitors = forms.ModelMultipleChoiceField(
        queryset = models.CompetitorModel.objects.filter(developer_competitor__site__in=['express-shina.ru', 'kolesatyt.ru', 'kolesa-darom.ru']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'), 
        widget = forms.CheckboxSelectMultiple(),                                                                                            ### initial не работает, пришлось тупо влесть в queryset. тупо аж капец                                        #####
    )

class DeflectionInputForm(forms.Form):
    deflection_data = forms.FloatField(label='размер снимаемой торговой надбавки, (%)', required=None, max_value=100, min_value=0, 
    widget=forms.NumberInput(attrs={'id': 'deflection_data', 'step': "0.01"}))

class PaginationInputForm(forms.Form):
    pagination_data = forms.IntegerField(label='количество выводимых позиций (1-25)', required=None, max_value=25, min_value=0, 
    widget=forms.NumberInput(attrs={'id': 'pagination_data', 'step': "1"}))


class CurrencyDateInputForm(forms.Form):
    #chosen_date_for_currency = forms.DateField(widget=forms.DateInput(format='%m-%Y-%d'))
    chosen_date_for_currency = forms.DateField(widget=forms.SelectDateWidget(years=range(2022,2024)),
    label='курс НБ РБ на дату:',
    initial='2022-7-7'

    )

    
    #initial=datetime.date.today())  
    
    

