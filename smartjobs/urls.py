from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import hello

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include([
        path('', include('djoser.urls')),
        path('', include('djoser.urls.jwt')),
        path('', include('users.urls')),  # ضفنا users ضمن auth
    ])),

    path('api/jobs/', include('jobs.urls')),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/hello/', hello),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)