from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

handler404 = 'contracts.views.error_404'

urlpatterns = [
    path("", include('contracts.urls')),
    path("notification/", include('notification.urls')),
    path("admin/", admin.site.urls),
    path('invoice/', include('invoice.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
