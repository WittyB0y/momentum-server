from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from momentumServer import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
