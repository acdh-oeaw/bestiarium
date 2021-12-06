import lxml.etree as ET

from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from .omenview import (
    all_chapters,
    get_chapter,
    get_omen,
    omens_in_chapter
)

from .models import PhilComment


def chapters(request):
    template_name = "omens/chapters.html"
    context = all_chapters()
    return render(request, template_name, context)


def chapter_detail(request, chapter_name):
    template_name = "omens/chapter_full.html"
    chapter = get_chapter(chapter_name=chapter_name)
    context = {
        "tei": chapter.safe_tei,
        "chapter_name": chapter_name,
        "xsldoc": "chapter_detail",
    }
    return render(request, template_name, context)


def chapter_overview(request, chapter_name):
    template_name = "omens/chapter_structure.html"
    chapter = get_chapter(chapter_name=chapter_name)
    context = {
        "chapter": chapter,
    }
    return render(request, template_name, context)


def chapter_layout(request, chapter_name):
    template_name = "omens/chapter_full.html"
    chapter = get_chapter(chapter_name=chapter_name)
    omens = omens_in_chapter(chapter_name)
    num_omens = len(omens.get("omens")) if omens else 0
    xslt_doc = ET.parse("./omens/templates/omens/threecolumn.xsl")
    transform = ET.XSLT(xslt_doc)
    print("#########################start#######################")
    xml = ET.fromstring(chapter.full_tei_string)
    html = transform(xml)
    print("#########################stop#######################")
    context = {
        "tei": html,
        "chapter_name": chapter_name,
        "animal": chapter.animal,
        "num_omens": num_omens,
        "witnesses": [],
        "xsldoc": "threecolumn",
        "author": chapter.author if chapter.author else "Nicla De Zorzi et al.",
    }
    return render(request, template_name, context)


def chapter_tei(request, chapter_name):
    """
    Javascript cannot handle line breaks in a string!\
    And single quotes must be escaped because the template string is enclosed in single quotes.
    """
    template_name = "omens/chapter_full.html"
    chapter = get_chapter(chapter_name=chapter_name)
    context = {
        "tei": chapter.safe_tei,
        "chapter_name": chapter_name,
        "xsldoc": "tei2html",
    }
    return render(request, template_name, context, content_type="text/html")


def xsldoc(request, xsl_name):
    template_name = f"omens/{xsl_name}.xsl"
    return render(request, template_name, {}, content_type="application/xml")


def chapter_tei_raw(request, chapter_name):
    chapter = get_chapter(chapter_name=chapter_name)
    return HttpResponse(chapter.full_tei_string, content_type="application/xml")


# def omen_detail(request, omen_id):
#     template_name = "omens/omen_detail.html"
#     context = omen_hypernyms(omen_id)
#     return render(request, template_name, context, content_type="text/html")


def omen_tei_raw(request, omen_id):
    template_name = "omens/tei.xml"
    omen = get_omen(omen_id)
    context = {"tei": omen.full_tei_string}
    return render(request, template_name, context, content_type="text/xml")


def omen_tei(request, omen_id):
    template_name = "omens/omen_full.html"

    omen = get_omen(omen_id)
    if omen:
        xslt_doc = ET.parse("./omens/templates/omens/threecolumn.xsl")
        transform = ET.XSLT(xslt_doc)
        xml = ET.fromstring(omen.full_tei_string)
        html = transform(xml)
        try:
            comment_base = PhilComment.objects.get(omen=omen)
        except ObjectDoesNotExist:
            comment_base = None
        if comment_base:
            com = comment_base.comment
        else:
            com = None
        context = {
            "html": html,
            "comment": com,
            "omen_id": omen.xml_id,
            "omen_num": omen.omen_num,
            "chapter_name": omen.chapter.chapter_name,
            "xsldoc": "threecolumn",
            "author": omen.chapter.author
            if omen.chapter.author
            else "Nicla De Zorzi et al.",
        }
        return render(request, template_name, context, content_type="text/html")

    raise Http404


# @login_required
# def edit_translation(request, omen_id, translation_id):
#     try:
#         updated_data = request.GET.dict()
#         logging.debug("%s - %s", translation_id, updated_data)
#         update_translation(translation_id, updated_data.get(f"input_{translation_id}"))
#         messages.add_message(request, messages.SUCCESS, "Your changes have been saved!")
#     except Exception as e:
#         logging.error(repr(e))
#         messages.add_message(
#             request,
#             messages.ERROR,
#             "Something went wrong!",
#             extra_tags="danger",
#         )
#     return omen_detail(request, omen_id)
    # template_name = 'omens/omen_detail.html'
    # context = omen_hypernyms(omen_id)
    # return render(request, template_name, context, content_type='text/html')

    # return redirect(omen_detail(request, omen_id))
