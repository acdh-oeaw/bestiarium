from django.shortcuts import render

# Create your views here.
from .models import Chapter, Omen, Reconstruction, Translation


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
    '''
    available = Product.objects.filter(packaging__available=True)
subcategories = SubCategory.objects.filter(category_id=<id_of_male>)
products = available.filter(subcategory_id__in=subcategories)

lookup = {'packaging_available': True, 'subcategory__category_id__in': ['ids of males']}
product_objs = Product.objects.filter(**lookup)

    '''
    translations = {}
    for reading in Reconstruction.objects.filter(omen__omen_id=omen.omen_id):
        print(reading)
        translations[reading.reconstruction_id] = {}
        records = Translation.objects.filter(
            reconstruction__reconstruction_id=reading.reconstruction_id)
        for record in records:
            if record.segment.segment_id.endswith('P'):
                translations[reading.reconstruction_id][
                    'PROTASIS'] = record.translation_txt
            if record.segment.segment_id.endswith('A'):
                translations[reading.reconstruction_id][
                    'APODOSIS'] = record.translation_txt

    context = {'data': {'omen': omen, 'translations': translations}}
    return render(request, template_name, context, content_type='text/html')


def omen_tei(request, omen_id):
    template_name = 'omens/tei.xml'
    omen = Omen.objects.filter(omen_id=omen_id)[0]
    context = {'tei': omen.tei}
    return render(request, template_name, context, content_type='text/xml')
