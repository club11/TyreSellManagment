from dataclasses import fields
from pyexpat import model
from django import forms
from . import models


from dictionaries import models as dictionaries_models



class TyreCardForm(forms.ModelForm):
    class Meta:
        model = models.TyreCard
        tyre = forms.ModelChoiceField(queryset=models.TyreCard.objects.all(), required=True)
        fields = {
            'tyre',
            'serie_date',
            'picture',
        }


    

class TyreForm(forms.ModelForm):
    class Meta:
        model = models.Tyre
        fields = {
            'tyre_model',
            'tyre_size',
            'tyre_type',
        }