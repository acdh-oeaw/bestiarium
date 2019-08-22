from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Spreadsheet


class UploadSpreadSheet(forms.Form):
    upload_file = forms.FileField()

    class Meta:
        model = Spreadsheet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'p-3'
        self.helper.add_input(Submit('submit', 'SAVE', css_class='btn btn-primary btn-lg btn-block'),)
