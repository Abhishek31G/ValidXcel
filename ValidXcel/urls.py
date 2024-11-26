from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from valix.views import upload_file_view, view_data, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='home'),
    path('upload/', upload_file_view, name='upload_file'),
    path('view/<uuid:file_id>/', view_data, name='view_data'),
    path('dashboard/', dashboard_view, name='dashboard')
]
if settings.DEBUG: 
    urlpatterns += static (settings.MEDIA_URL, 
                           document_root=settings.MEDIA_ROOT) 
urlpatterns += staticfiles_urlpatterns()
