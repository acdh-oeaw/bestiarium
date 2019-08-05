import os

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.core.files.storage import default_storage

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .forms import UploadSpreadSheet
from xl2tei.omensworkbook import OmensWorkbook


# Create your views here.

class UploadSpreadSheet(FormView):
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
        context = super(UploadSpreadSheet, self).get_context_data(**kwargs)
        cd = form.cleaned_data
        uploaded_file = cd.get('uploaded_file')

        filename = 'whatever.xls'
        
        with default_storage.open(filename, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        print(destination)
        wb = OmensWorkbook(destination.name )
        print(wb)
        '''
        context['unzip_path'] = extract_path
        zf = zipfile.ZipFile(zipped, 'r')
        extracted = zf.extractall(extract_path)
        for x in zf.infolist():
            if (x.filename).endswith('.jp2'):
                print(x.filename)
                new_img = Image.objects.create(
                    directory=cd['filepath'],
                    custom_filename=x.filename)
                # new_img.save()
                # x.extract(x.filename, [context['unzip_path']])

        context['extract_path'] = extract_path
        context['zipped'] = zf.infolist()
        '''
        context['extract_path'] = 'Whatever'

        return render(self.request, self.template_name, context)

        
