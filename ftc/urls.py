
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

from django.conf.urls import handler404, handler500

from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('ikpixels.urls')),
    path('', include('music_nation.urls')),
    path('Store', include('Store.urls')),
    path('Event', include('Event.urls')),
    path('ikpixels', include('ikpixels.urls')),
    path('account', include('account.urls'))
]


handler404 = views.error_404
handler500 = views.error_500


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)