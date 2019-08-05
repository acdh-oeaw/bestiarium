from django.conf.urls import url
from . import views

app_name = 'upload'

urlpatterns = [
    url(r'^single$', views.UploadSpreadSheet.as_view(), name='upload_file'),
]
