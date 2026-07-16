from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import config.admin  # noqa: F401 — настройка заголовков админки

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.schools.urls')),
    path('api/', include('apps.content.urls')),
    path('api/', include('apps.schedules.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
