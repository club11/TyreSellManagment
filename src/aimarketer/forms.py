from django import forms

class AIForm(forms.Form):
    ai_request = forms.CharField(
        max_length=1000,
        required=None,
        label='AI запрос',
    )
    file_fields = forms.FileField(
        allow_empty_file=None,
        required=None,
    )