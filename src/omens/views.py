from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Create your views here.
from .models import Omen
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
    template_name = 'omens/tei.xml'
    chapter = get_chapter(chapter_name=chapter_name)
    context = {'tei': chapter.tei}
    return render(request, template_name, context, content_type='text/xml')


def omen_detail(request, omen_id):
    template_name = 'omens/omen_detail.html'
    context = omen_hypernyms(omen_id)
    return render(request, template_name, context, content_type='text/html')


def omen_tei(request, omen_id):
    template_name = 'omens/tei.xml'
    omen = get_omen(omen_id)
    context = {'tei': omen.tei}
    return render(request, template_name, context, content_type='text/xml')


@login_required
def edit_translation(request, omen_id, translation_id):
    try:
        updated_data = request.GET.dict()
        print(translation_id, updated_data)
        update_translation(translation_id,
                           updated_data.get(f'input_{translation_id}'))
        messages.add_message(request, messages.SUCCESS,
                             'Your changes have been saved!')
    except Exception as e:
        print(repr(e))
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
