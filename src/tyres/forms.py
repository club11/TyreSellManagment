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