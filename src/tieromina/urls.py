from django.conf import settings
from django.conf.urls import handler404, include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

if 'bib' in settings.INSTALLED_APPS:
    from bib.api_views import ZotItemViewSet

router = routers.DefaultRouter()

if 'bib' in settings.INSTALLED_APPS:
    router.register(r'zotitems', ZotItemViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^info/', include('infos.urls', namespace='info')),
    url(r'^', include('webpage.urls', namespace='webpage')),
    url(r'^curator/', include('curator.urls', namespace='curator')),
    url(r'^omens/', include('omens.urls', namespace='omens')),
    url(r'^explore/', include('dataviz.urls', namespace='dataviz')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if 'bib' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^bib/', include('bib.urls', namespace='bib')), )

if 'sparql' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^sparql/', include('sparql.urls', namespace='sparql')), )

handler404 = 'webpage.views.handler404'
