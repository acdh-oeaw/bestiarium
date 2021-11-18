from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers


router = routers.DefaultRouter()

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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'webpage.views.handler404'
