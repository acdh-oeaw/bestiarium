from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import SenseTree, Upload


class UploadSpreadSheet(forms.Form):
    index_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
    omen_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
    ditto_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
    credits_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
    comments_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    class Meta:
        model = Upload
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        # self.helper.form_class = ''
        self.helper.form_class = "p-3"
        self.fields["index_files"].label = "Indices"
        self.fields["omen_files"].label = "Omens"
        self.fields["ditto_files"].label = "Dittos"
        self.fields["credits_files"].label = "Credits"
        self.fields["comments_files"].label = "Philological commentary"

        self.helper.label_class = "col-md-5"
        self.helper.field_class = "col-md-11"

        self.helper.add_input(
            Submit("submit", "SAVE", css_class="btn btn-primary btn-lg btn-block")
        )


class CurateSense(forms.Form):
    class Meta:
        model = SenseTree
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        # self.helper.form_class = ''
        self.helper.form_class = "p-3"

        self.helper.label_class = "col-md-1"
        self.helper.field_class = "col-md-11"

        self.helper.add_input(
            Submit("submit", "SAVE", css_class="btn btn-primary btn-lg btn-block"),
        )
