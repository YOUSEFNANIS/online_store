from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.urls import re_path
from django.views.decorators.cache import cache_control
from django.views.static import serve
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenRefreshView  
from users.views import CustomTokenObtainPairView, RefreshView

urlpatterns = [
    path(
        'robots.txt',
        lambda request: HttpResponse(
            'User-agent: *\nAllow: /\n',
            content_type='text/plain; charset=utf-8',
        ),
        name='robots_txt',
    ),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('messaging/', include('messaging.urls')),
    path('chat/', include('chatbot.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', RefreshView.as_view(), name='token_refresh'),
    path('signup/', include('users.urls')),
]

if settings.DEBUG:
    @cache_control(
        public=True,
        max_age=settings.MEDIA_CACHE_MAX_AGE,
        immutable=True,
    )
    def media_serve(request, path):
        return serve(request, path, document_root=settings.MEDIA_ROOT)

    urlpatterns.append(
        re_path(
            rf'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
            media_serve,
        )
    )

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
