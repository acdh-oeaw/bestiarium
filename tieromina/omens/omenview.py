'''
This acts as an interface between views.py and the model
'''
from .models import Chapter, Omen, Reconstruction, Translation


def all_chapters() -> dict:
    '''
    Returns all the chapters in the database
    TODO: Which order?
    '''
    all_chapters = Chapter.objects.all()
    return {'chapters': all_chapters}


def omens_in_chapter(chapter_name: str) -> dict:
    '''
    Returns the omens inside a given chapter
    '''
    chapter = Chapter.objects.filter(chapter_name=chapter_name)[0]
    omens = Omen.objects.order_by('omen_num').filter(chapter=chapter)
    return {'chapter': chapter, 'omens': omens}
