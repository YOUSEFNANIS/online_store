from .views import CustomerViewset, SellerViewset, LogoutView, getUserView, SellerListViewset, VerifyEmailView, ResendVerificationView, PasswordResetRequestView, PasswordResetConfirmView
from rest_framework.routers import SimpleRouter
from django.urls import path
router = SimpleRouter()
router.register('customer', CustomerViewset)
router.register('seller', SellerViewset)
router.register('sellers', SellerListViewset, basename='sellers')
router.register(r'get_id', getUserView, basename='get_id')
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
urlpatterns += router.urls