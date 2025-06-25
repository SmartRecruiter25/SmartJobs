from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from jobs import views as job_views

urlpatterns = [
    path('admin/', admin.site.urls),

   
    path('', job_views.jobs, name='home'),

   
    path('jobs/', include('jobs.urls')),
    
    path('api/', include('api.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)