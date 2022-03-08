import logging
import os
# import pandas as pd

from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views.generic.edit import FormView
from omens.creditsimporter import CreditsImporter
from omens.indeximporter import IndexImporter
from omens.omenimporter import OmenImporter
# from omens.coment_utils import import_comments

from .forms import UploadSpreadSheet
from .models import USTATUS, UTYPES, Upload

# from xl2tei.workbook import Workbook

logger = logging.getLogger(__name__)
# Create your views here.
UPLOAD_LOC = "/"


class UploadSpreadSheet(LoginRequiredMixin, FormView):
    template_name = "upload/upload_spreadsheet.html"
    form_class = UploadSpreadSheet
    success_url = "."
    upload_files = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.upload_files = {
            ftype: request.FILES.getlist(f"{ftype}_files") for ftype in UTYPES.ALL
        }

        report = []
        if self.is_valid():
            for ftype in UTYPES.ALL:
                for f in self.upload_files.get(ftype):
                    r = self.upload(ftype, f)
                    if r:
                        report.append(r)

            return self.form_valid(form, report=report)

        else:
            return self.form_invalid(form)

    def is_valid(self):
        num_files = sum(len(v) for _, v in self.upload_files.items())
        logger.debug("FOUND %s files", num_files)
        if not num_files:
            return False

        return True

    def form_invalid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        context["error"] = "You must upload at least one file."
        return render(self.request, self.template_name, context)

    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs.get("report"):
            context["report"] = kwargs.get("report")
        else:
            context["message"] = "Thank you! The upload was successful."

        return render(self.request, self.template_name, context)

    def upload(self, ftype, f):
        logger.debug("Uploading %s file %s", ftype, f._name)
        upload = self.record_upload(f, utype=ftype)
        report = None
        if ftype == UTYPES.INDEX_FILE:
            report = IndexImporter(f).save()
        elif ftype == UTYPES.OMEN_FILE:
            report = OmenImporter(f, upload).save()

        # elif ftype == UTYPES.COMMENTS_FILE:
        #     df = pd.read_excel(f, converters={'omen': str, 'omen': str})
        #     report = import_comments(df)

        elif ftype == UTYPES.DITTO_FILE:
            pass
        elif ftype == UTYPES.CREDITS_FILE:
            report = CreditsImporter(f).save()

        upload.report = report
        upload.ustatus = USTATUS.ERROR if report else USTATUS.SUCCESS
        upload.save()
        if report:
            return {f._name: report}

    def record_upload(self, uploaded_file, utype):
        """
        Creates a record of this file in the Upload model -
        regardless of whetrher the processing of successful
        """

        with default_storage.open(uploaded_file._name, "wb") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        filename = os.path.join(default_storage.location, uploaded_file._name)
        upload = Upload(
            name=uploaded_file._name,
            user=self.request.user.username,
            location=filename,
            utype=utype,
        )
        upload.save()
        return upload

    # def upload_omen_file(self, f):
    # FIXME: Delete this
    #     logger.debug("Uploading omen file %s", f._name)
    #     upload = self.record_upload(f, utype=UTYPES.OMEN_FILE)
    #     # Extract omens
    #     try:
    #         # Add/create a chapter
    #         chapter = Chapter()
    #         chapter_db = chapter.export_to_tei(f)
    #         # Save upload record
    #         logger.debug("Default storage: %s", f)
    #         upload.ustatus = USTATUS.SUCCESS
    #     except Exception as e:
    #         report = {f._name: repr(e)}
    #         upload.report = report
    #         upload.ustatus = USTATUS.ERROR
    #         logger.error(repr(e))
    #         # raise

    #     upload.save()
    #     return upload.report
