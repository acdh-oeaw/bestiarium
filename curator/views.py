import logging
import os
import pandas as pd

from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views.generic.edit import FormView
from omens.chapter import Chapter
from omens.creditsimporter import CreditsImporter
from omens.indeximporter import IndexImporter
from omens.omenimporter import OmenImporter
from omens.coment_utils import import_comments

from .forms import UploadSpreadSheet
from .models import USTATUS, UTYPES, Upload

# from xl2tei.workbook import Workbook

logger = logging.getLogger(__name__)
# Create your views here.
UPLOAD_LOC = "/"


# def words():
#     translations = Translation.objects.filter(lang="en")
#     omen_data = defaultdict(dict)
#     for t in translations:
#         if not t.translation_txt.strip():
#             continue
#         omen_data[t.reconstruction.reconstruction_id][
#             t.segment.segment_type
#         ] = t.translation_txt.replace("[", "").replace("]", "")
#         omen_data[t.reconstruction.reconstruction_id][
#             "omen_id"
#         ] = t.segment.omen.omen_id
#         omen_data[t.reconstruction.reconstruction_id][
#             "chapter"
#         ] = t.segment.omen.chapter.chapter_name

#     data = []
#     for recon, info in omen_data.items():
#         data.append(
#             {
#                 "omen": info.get("omen_id"),
#                 "chapter": info.get("chapter"),
#                 "reconstruction": recon,
#                 "protasis": info.get("PROTASIS", ""),
#                 "apodosis": info.get("APODOSIS", ""),
#             }
#         )
#     return data


# def loom(request, outer, inner):
#     print(outer, inner)
#     data = words()
#     return JsonResponse(data, safe=False)


# def deep_parse(nested_dict, root=False):
#     unique_nodes = []
#     if not root:
#         # add value
#         unique_nodes = [nested_dict.get("value")]

#     children = []

#     if nested_dict.get("children"):
#         for child in nested_dict.get("children"):
#             unique_nodes.extend(deep_parse(child))

#     return list(set(unique_nodes))


# @login_required
# def save_senses(request, translation_id, word):  #
#     dicted = loads(request.body)
#     unique_nodes = deep_parse(dicted, root=True)

#     trs = Translation.objects.get(translation_id=translation_id)

#     # Save sense tree
#     try:
#         with transaction.atomic():
#             try:
#                 sTree_in_db = SenseTree.objects.get(word=word, translation=trs)
#                 sTree_in_db.delete()
#             except SenseTree.DoesNotExist as dne:
#                 pass

#             sTree = SenseTree.objects.create(
#                 word=word, curated_sense=dumps(dicted), translation=trs
#             )  # TODO: Add user
#             for node in unique_nodes:
#                 Sense.objects.create(sense_uri=node, sTree=sTree)

#             return HttpResponse("Saved")
#     except OperationalError as oe:
#         logging.error(repr(oe))
#         return HttpResponse("Exception occured")


# def wordsense(request, translation_id, word):
#     # Check if a Sense Tree exists already
#     trs = Translation.objects.get(translation_id=translation_id)
#     try:
#         stree_from_db = SenseTree.objects.get(word_root=word)
#     except SenseTree.DoesNotExist as dne:
#         stree_from_db = SenseTree.objects.filter(word_root=word).first()

#     data = None
#     if stree_from_db:
#         curated_sense = stree_from_db.curated_sense
#         if curated_sense:
#             data = loads(curated_sense)

#     if not data:
#         data = synset_tree(word)

#     return JsonResponse(data, safe=False)


# def sensed3(request, word):
#     return JsonResponse(synset_tree(word), safe=False)


# @login_required
# def view_senses(request, page=1, chapter=""):
#     template_name = "curator/segments.html"
#     all_translations = []
#     paginator = Paginator(
#         Translation.objects.filter(reconstruction__omen__chapter__chapter_name=chapter),
#         3,
#         1,
#     )
#     page_obj = paginator.get_page(page)

#     # for t in Translation.objects.all():
#     #     sense_data = {}
#     #     sense_data['translation'] = t
#     #     sense_data['hypernyms'] = get_hypernyms(t.translation_txt)
#     #     all_translations.append(sense_data)
#     # paginator = Paginator(all_translations, 20, 1)
#     # page_obj = paginator.get_page(page)
#     return render(
#         request,
#         template_name,
#         {
#             "page_obj": page_obj,
#         },
#     )


# @login_required
# def edit_sense(request, word):
#     template_name = "curator/editsenses.html"
#     segment_info = []
#     translations = Translation.objects.filter(lang="en")
#     for t in translations:
#         clean_t = t.translation_txt.replace("[", "").replace("]", "")
#         if word in clean_t:
#             segment_info.append(
#                 {"omen": t.segment.omen.omen_id, "segment": t.translation_txt}
#             )
#     return render(request, template_name, {"segments": segment_info, "word": word})


# @login_required
# def curate_senses(request):
#     template_name = "curator/curate_senses.html"
#     # Get all words that are unattached to senses
#     translations = Translation.objects.filter(lang="en")
#     words = defaultdict(int)
#     for t in translations:
#         for w in t.translation_txt.split():
#             words[w] += 1

#     words = {
#         k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True)
#     }
#     return render(request, template_name, {"words": words})


# @login_required
# def edit_translation(request, page, translation_id):
#     try:
#         updated_data = request.GET.dict()
#         db_handle = Translation.objects.get(translation_id=translation_id)
#         db_handle.translation_txt = updated_data.get(f"input_{translation_id}")
#         db_handle.save()
#         messages.add_message(request, messages.SUCCESS, "Your changes have been saved!")
#     except Exception as e:
#         logging.error(repr(e))
#         messages.add_message(
#             request,
#             messages.ERROR,
#             "Something went wrong!",
#             extra_tags="danger",
#         )
#         # view_senses(request)
#     return redirect(request.META["HTTP_REFERER"])


# class CurateSense(LoginRequiredMixin, FormView):
#     template_name = "curator/curate.html"
#     omen_id = None
#     form_class = CurateSense
#     success_url = "."

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()

#         self.helper.form_tag = True
#         self.helper.form_class = "form-horizontal"
#         self.helper.label_class = "col-md-1"
#         self.helper.field_class = "col-md-11"
#         # self.helper.add_input(Submit('submit', 'save'), )

#     def form_valid(self, form, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cd = form.cleaned_data
#         #    return render(request, template_name, context)
#         return render(self.request, self.template_name, context)


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

        elif ftype == UTYPES.COMMENTS_FILE:
            df = pd.read_excel(f)
            report = import_comments(df)

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
