from dataclasses import field, fields
from django import forms
from dictionaries import models
from django.core.exceptions import ValidationError
#
from validators.validators import competitor_num_validator
#
##class FilterForm(forms.Form):            
##    #data = forms.CharField(label='контактные данные', widget=forms.TimeInput, disabled=True, required=None,) # вах! изучить
##    competitor= forms.CharField(label='произодители', required=None, max_length=20,  validators=[competitor_num_validator])
#
#class FilterForm(forms.ModelForm):
#    class Meta:
#        model = models.CompetitorModel
#        fields = {
#            'competitor_name',           
#        }



class FilterForm(forms.Form):
    competitors = forms.ModelMultipleChoiceField(
        #queryset = models.CompetitorModel.objects.all(), 
        queryset = models.CompetitorModel.objects.all().values_list("competitor_name", flat=True),
        widget = forms.CheckboxSelectMultiple(),                                                                                            ### initial не работает, пришлось тупо влесть в queryset. тупо аж капец
        #initial={'cometitors':querysetofinitialvalues},                                                                                    #####
        #initial={"multi_field": [cat for cat in models.CompetitorModel.objects.all().values_list("competitor_name", flat=True)]}           #####
        #initial=models.CompetitorModel.objects.all().values_list("competitor_name", flat=True)                                             #####
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


    

    
