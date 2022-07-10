from dataclasses import fields
from pyexpat import model
from django import forms
from . import models

class TyreSizeForm(forms.ModelForm):
    class Meta:
        model = models.TyreSizeModel
        fields = {
            'tyre_size',
        }


class ModelNameForm(forms.ModelForm):
    class Meta:
        model = models.ModelNameModel
        fields = {
            'model',
        }