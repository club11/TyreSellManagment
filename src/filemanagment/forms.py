from django import forms
import datetime



class ImportDataForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=None,
        label='Импортировать данные (модель/ типоразмер/ параметры',
    )
    file_fields = forms.FileField(
        allow_empty_file=None,
    )

class ImportSalesDataForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=None,
        label='Импортировать данные о реализации',
    )
    file_fields = forms.FileField(
        allow_empty_file=None,
    )

from datetime import timedelta
class ImportTimeForm(forms.Form):
  time_task_a = forms.TimeField(
      widget=forms.TimeInput(attrs={'class': 'unbold-form'}, format='%H:%M'), 
      initial=datetime.time(),
      label='Установить время запуска парсинга сайтов',
  )
  time_task_b = forms.TimeField(
      widget=forms.TimeInput(attrs={'class': 'unbold-form'}, format='%H:%M'), 
      initial=datetime.time(),
      label='Установить время считывания данных из импотируемого файла',
  )