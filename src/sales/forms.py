from django import forms
from . import models

class SalesForm(forms.ModelForm):
    class Meta:
        model = models.Sales
        fields = {
            'tyre',
            'date_of_sales',
            'contragent',
            'sales_value',            
        }
    