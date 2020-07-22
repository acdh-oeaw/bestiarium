from xml.etree import ElementTree as ET

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from .omenview import (all_chapters, get_chapter, get_omen, omen_hypernyms,
                       omens_in_chapter, update_translation)


def chapters(request):
    template_name = 'omens/chapters.html'
    context = all_chapters()
    return render(request, template_name, context)


def chapter_detail(request, chapter_name):
    template_name = 'omens/chapter_detail.html'
    context = omens_in_chapter(chapter_name)
    return render(request, template_name, context)


def chapter_tei(request, chapter_name):
    '''
    Javascript cannot handle line breaks in a string! And single quotes must be escaped because the template string is enclosed in single quotes.
    '''
    template_name = 'omens/embedded.html'
    chapter = get_chapter(chapter_name=chapter_name)
    context = {'tei': chapter.safe_tei, 'chapter_name': chapter_name}
    return render(request, template_name, context, content_type='text/html')


def chapter_xsl(request, chapter_name):
    template_name = 'omens/tei2html.xsl'
    return render(request, template_name, {}, content_type='application/xml')


def omen_xsl(request, omen_id):
    template_name = 'omens/tei2html.xsl'
    return render(request, template_name, {}, content_type='application/xml')


def chapter_tei_raw(request, chapter_name):
    template_name = 'omens/tei.xml'
    chapter = get_chapter(chapter_name=chapter_name)
    context = {'tei': chapter.tei}
    return render(request, template_name, context, content_type='text/xml')


def omen_detail(request, omen_id):
    template_name = 'omens/omen_detail.html'
    context = omen_hypernyms(omen_id)
    return render(request, template_name, context, content_type='text/html')


def omen_tei_raw(request, omen_id):
    template_name = 'omens/tei.xml'
    omen = get_omen(omen_id)
    context = {'tei': omen.tei}
    return render(request, template_name, context, content_type='text/xml')


def omen_tei(request, omen_id):
    template_name = 'omens/embedded.html'
    try:
        omen = get_omen(omen_id)
        context = {
            'tei': omen.chapter.safe_tei,
            'omen_id': omen.omen_id,
            'omen_num': omen.omen_num,
            'chapter_name': omen.chapter.chapter_name
        }
        return render(request,
                      template_name,
                      context,
                      content_type='text/html')
    except Exception as e:
        raise Http404


@login_required
def edit_translation(request, omen_id, translation_id):
    try:
        updated_data = request.GET.dict()
        logging.debug("%s - %s", translation_id, updated_data)
        update_translation(translation_id,
                           updated_data.get(f'input_{translation_id}'))
        messages.add_message(request, messages.SUCCESS,
                             'Your changes have been saved!')
    except Exception as e:
        logging.error(repr(e))
        messages.add_message(
            request,
            messages.ERROR,
            'Something went wrong!',
            extra_tags='danger',
        )
    return omen_detail(request, omen_id)
    # template_name = 'omens/omen_detail.html'
    # context = omen_hypernyms(omen_id)
    # return render(request, template_name, context, content_type='text/html')

    # return redirect(omen_detail(request, omen_id))
