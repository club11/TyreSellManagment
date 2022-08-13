from django import forms

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
    