from django.contrib import admin

# Register your models here.
from .models import Tablet

def all_spreadsheets(obj):
    print(dir(obj.spreadsheet))
    return (', '.join([str(s[1].strip('.xls')) for s in obj.spreadsheet.values_list()]))


class TabletAdmin(admin.ModelAdmin):

    list_display = ('tablet_id', 'ctime', all_spreadsheets)

    



admin.site.register(Tablet, TabletAdmin)
