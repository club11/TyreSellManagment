from dataclasses import fields
from pyexpat import model
from django import forms
from . import models

class TyreCardForm(forms.ModelForm):
    class Meta:
        model = models.TyreCard
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