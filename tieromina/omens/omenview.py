'''
This acts as an interface between views.py and the model
'''
import logging

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
    chapter = get_chapter(chapter_name)
    omens = Omen.objects.order_by('omen_num').filter(chapter=chapter)
    message = f'Cound not find chapter {chapter_name}' if not chapter else ''
    return {'chapter': chapter, 'omens': omens, 'error': message}


def get_chapter(chapter_name: str) -> Chapter:
    try:
        return Chapter.objects.filter(chapter_name=chapter_name)[0]
    except IndexError:
        logging.error('Could not find chapter "%s"', chapter_name)
        return None
