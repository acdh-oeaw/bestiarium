from django.urls import re_path

from . import views

app_name = "curator"

urlpatterns = [
    re_path(r"^upload$", views.UploadSpreadSheet.as_view(), name="upload_file"),
]
