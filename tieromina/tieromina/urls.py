from django.conf.urls import url, include, handler404
from django.contrib import admin
from django.conf import settings
from rest_framework import routers


if 'bib' in settings.INSTALLED_APPS:
    from bib.api_views import ZotItemViewSet

router = routers.DefaultRouter()

if 'bib' in settings.INSTALLED_APPS:
    router.register(r'zotitems', ZotItemViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^info/', include('infos.urls', namespace='info')),
    url(r'^', include('webpage.urls', namespace='webpage')),
    url(r'^upload/', include('upload.urls', namespace='upload')),

]

if 'bib' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^bib/', include('bib.urls', namespace='bib')),
    )

if 'sparql' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^sparql/', include('sparql.urls', namespace='sparql')),
    )

handler404 = 'webpage.views.handler404'
