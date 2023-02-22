from dataclasses import field, fields
from django import forms
from dictionaries import models
from . import models as prices_models
from django.core.exceptions import ValidationError

from validators.validators import competitor_num_validator




class FilterForm(forms.Form):
    competitors = forms.ModelMultipleChoiceField(
        queryset = models.CompetitorModel.objects.filter(developer_competitor__site__in=['onliner.by', 'bagoria.by', 'autoset.by']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'), 
        widget = forms.CheckboxSelectMultiple(),                                                                                            ### initial не работает, пришлось тупо влесть в queryset. тупо аж капец                                        #####
    )

    #def __init__(self, *args, **kwargs):                                                                                                   #####
    #    super(FilterForm, self).__init__(*args, **kwargs)                                                                                  #####
    #    print(self.fields["competitors"].initial, 'KKKK')                                                                                  #####
    #    a = self.fields["competitors"].initial = (models.CompetitorModel.objects.all().values_list('competitor_name', flat=True))          #####
    #    print(a, 'рунная фраза')                                                                                                           #####
    #    self.fields["competitors"].initial = (models.CompetitorModel.objects.all().values_list('competitor_name', flat=True)               #####
    #    )

    #def competitor_num_validator(self, value):                                                     ДОРАБОТАТЬ ВАЛИДАЦИЮ 3 и более выбранных производителя
    #    less_than_three = value
    #    if less_than_three > 3:
    #        raise ValidationError(
    #            "до трех производителей",
    #        )
    #    return value 
    # 
class FilterRussiaForm(forms.Form):
    competitors = forms.ModelMultipleChoiceField(
        queryset = models.CompetitorModel.objects.filter(developer_competitor__site__in=['express-shina.ru', 'kolesatyt.ru', 'kolesa-darom.ru']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'), 
        widget = forms.CheckboxSelectMultiple(),                                                                                            ### initial не работает, пришлось тупо влесть в queryset. тупо аж капец                                        #####
    )

class DeflectionInputForm(forms.Form):
    deflection_data = forms.FloatField(label='размер снимаемой торговой надбавки, (%)', required=None, max_value=100, min_value=0, 
    widget=forms.NumberInput(attrs={'id': 'deflection_data', 'step': "0.01"}))