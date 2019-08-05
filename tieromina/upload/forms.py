from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Spreadsheet


class UploadSpreadSheet(forms.Form):
    filepath = forms.CharField(label='path to file', max_length=250, required=False)
    uploaded_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-1'
        self.helper.field_class = 'col-md-11'
        self.helper.add_input(Submit('submit', 'save'),)
