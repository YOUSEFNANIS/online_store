from .views import CustomerViewset, SellerViewset, LogoutView, getUserView
from rest_framework.routers import SimpleRouter
from django.urls import path
router = SimpleRouter()
router.register('customer', CustomerViewset)
router.register('seller', SellerViewset)
router.register(r'get_id', getUserView, basename='get_id')
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]
urlpatterns += router.urls