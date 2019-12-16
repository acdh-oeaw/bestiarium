from django.shortcuts import render

# Create your views here.
from .models import Chapter, Omen


def chapters(request):
    template_name = 'omens/chapters.html'
    all_chapters = Chapter.objects.all()
    context = {'chapters': all_chapters}
    return render(request, template_name, context)


def chapter_detail(request, chapter_name):
    template_name = 'omens/chapter_detail.html'
    chapter_detail = Chapter.objects.filter(chapter_name=chapter_name)[0]
    omens = Omen.objects.order_by('omen_num').filter(chapter=chapter_detail)
    context = {'chapter': chapter_detail, 'omens': omens}
    return render(request, template_name, context)


def chapter_tei(request, chapter_name):
    template_name = 'omens/tei.xml'
    chapter = Chapter.objects.filter(chapter_name=chapter_name)[0]
    context = {'tei': chapter.tei}
    return render(request, template_name, context, content_type='text/xml')


def omen_detail(request, omen_id):
    template_name = 'omens/omen_detail.html'
    omen = Omen.objects.filter(omen_id=omen_id)[0]
    context = {'data': {'omen': omen}}
    return render(request, template_name, context, content_type='text/html')


def omen_tei(request, omen_id):
    template_name = 'omens/tei.xml'
    omen = Omen.objects.filter(omen_id=omen_id)[0]
    context = {'tei': omen.tei}
    return render(request, template_name, context, content_type='text/xml')
