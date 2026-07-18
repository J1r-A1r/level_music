from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Prefix all our music app URLs with /api/
    path('api/', include('music.urls')),
]

# This is CRITICAL for serving uploaded audio files and images during development!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)