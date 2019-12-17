'''
This acts as an interface between views.py and the model
'''
from .models import Chapter, Omen, Reconstruction, Translation


def all_chapters():
    '''
    Returns all the chapters in the database
    TODO: Which order?
    '''
    all_chapters = Chapter.objects.all()
    return {'chapters': all_chapters}
