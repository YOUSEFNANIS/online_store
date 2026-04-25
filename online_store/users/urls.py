from .views import customer_viewset, seller_viewset, LogoutView, getUserView
from rest_framework.routers import SimpleRouter
from django.urls import path
router = SimpleRouter()
router.register('customer', customer_viewset)
router.register('seller', seller_viewset)
router.register(r'get_id', getUserView, basename='get_id')
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]
urlpatterns += router.urls