from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', include('empl_database.urls')),
    path('admin/', admin.site.urls),
    path("logout/", lambda _request: redirect("/admin/logout", permanent=False)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
