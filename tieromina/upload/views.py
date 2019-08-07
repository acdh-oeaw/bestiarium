import os, logging

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.core.files.storage import default_storage
from django.contrib.auth.mixins import LoginRequiredMixin

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .forms import UploadSpreadSheet
from xl2tei.omensworkbook import OmensWorkbook
from .models import Spreadsheet

# Create your views here.
UPLOAD_LOC = '/'

class UploadSpreadSheet(LoginRequiredMixin, FormView):
    template_name = 'upload/upload_spreadsheet.html'
    form_class = UploadSpreadSheet
    success_url = '.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-1'
        self.helper.field_class = 'col-md-11'
        self.helper.add_input(Submit('submit', 'save'),)
        
    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        cd = form.cleaned_data
        uploaded_file = cd.get('upload_file')
        context['filename'] = uploaded_file._name
        filename = uploaded_file._name
        with default_storage.open(filename, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            wb = OmensWorkbook(destination.name )
            spreadsheet = Spreadsheet(name=uploaded_file)
            spreadsheet.save()
            
            wb.save_to_db(spreadsheet)
        except Exception as e:            
            context['error'] = repr(e)
            # raise
            
        return render(self.request, self.template_name, context)

        
