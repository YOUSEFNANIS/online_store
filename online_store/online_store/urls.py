from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView  
from users.views import CustomTokenObtainPairView, RefreshView
#import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('chat/', include('chatbot.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', RefreshView.as_view(), name='token_refresh'),
    path('signup/', include('users.urls')),
    #path("__debug__/", include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
