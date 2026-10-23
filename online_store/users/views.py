
from . import emails
from .models import seller, customer, User
from django.contrib.auth.tokens import default_token_generator
from online_store.validator import validate_password
from .serializer import CustomerSerializer, SellerSerializer, SellerListSerializer
from online_store.permissions import IsOwnerOrAdmin, IsCustomer
from core.order_flow import owner_of
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, FloatField, IntegerField, OuterRef, Subquery
from django.db.models.functions import Coalesce

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Pull the tokens from the JSON response body
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        if access_token:
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,     # Always use True in production (HTTPS)
                samesite='Lax',
                path= '/'
            )
            
        if refresh_token:
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )

        del response.data['access']
        del response.data['refresh']

        User = get_user_model()
        username = request.data.get('username')
        user = User.objects.get(username=username)

        if hasattr(user, 'customer'):
            response.data['user_type'] = 'customer'
        else :
            response.data['user_type'] = 'seller'
        return response


class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        request.data["refresh"] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)

            access_token = response.data.get("access")
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            del response.data['access']
            return response

        except Exception:
            return Response({"detail": "Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")

            if refresh_token:
                token = RefreshToken(refresh_token)

            response = Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_200_OK
            )

            # Delete cookies
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return response

        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

class getUserView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        # owner_of reads customer_pk / seller_pk from the auth query, with a fallback lookup
        # for other auth paths (e.g. force_authenticate in tests).
        role, pk = owner_of(request.user)
        if role == 'customer':
            user_object = customer.objects.get(pk=pk)
            id = getattr(user_object, 'id', "Default Value")
            url = user_object.profile_image.url if user_object.profile_image else None
            return Response({
            "id": id,
            "first_name": request.user.first_name,
            "date_joined": request.user.date_joined,
            "email_verified": request.user.email_verified,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone_number": getattr(user_object, 'phone_number', None),
            'profile_image': url,
            })
        
        elif role == 'seller':
            user_object = seller.objects.get(pk=pk)
            id = getattr(user_object, 'id', "Default Value")
            url = user_object.profile_image.url if user_object.profile_image else None
            store_url = user_object.store_image.url if user_object.store_image else None
            return Response({
                "id": id,
                "first_name": request.user.first_name,
                "date_joined": request.user.date_joined,
                "email_verified": request.user.email_verified,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "balance": getattr(user_object, 'balance', None),
                "phone_number": getattr(user_object, 'phone_number', None),
                'profile_image': url,
                'store_name': user_object.store_name,
                'store_image': store_url,
            })
        return Response({'detail': 'No customer or seller profile.'}, status=status.HTTP_404_NOT_FOUND)

class CustomerViewset(ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = customer.objects.order_by('id')
    serializer_class = CustomerSerializer

class SellerViewset(ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = seller.objects.order_by('id')
    serializer_class = SellerSerializer

def seller_directory_queryset():
    from core.models import product, Review
    # Correlated subqueries: no product x review join fan-out, no GROUP BY, and
    # the pagination COUNT drops them since it does not use them.
    seller_products = product.objects.filter(seller=OuterRef('pk')).order_by().values('seller').annotate(total=Count('pk')).values('total')
    seller_reviews = Review.objects.filter(product__seller=OuterRef('pk')).order_by().values('product__seller')
    return (
        seller.objects
        .only('id', 'store_name', 'store_image')
        .annotate(
            product_count=Coalesce(Subquery(seller_products, output_field=IntegerField()), 0),
            rating_count=Coalesce(Subquery(seller_reviews.annotate(total=Count('pk')).values('total'), output_field=IntegerField()), 0),
            rating_avg=Subquery(seller_reviews.annotate(average=Avg('rating')).values('average'), output_field=FloatField()),
        )
        .order_by('store_name')
    )


class SellerListViewset(ReadOnlyModelViewSet):
    # Customer-facing directory; store identity only (no owner name/email/phone/balance).
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = SellerListSerializer

    def get_queryset(self):
        return seller_directory_queryset()


class _AuthEmailView(APIView):
    permission_classes = []
    authentication_classes = []
    throttle_scope = 'auth_email'
    pagination_class = None


class VerifyEmailView(_AuthEmailView):
    def post(self, request):
        user = emails.user_from_uid(request.data.get('uid', ''))
        if user is None or not emails.email_verification_token.check_token(user, request.data.get('token', '')):
            return Response({'detail': 'This verification link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        user.email_verified = True
        user.save(update_fields=['email_verified'])
        return Response({'detail': 'Email verified.'})


class ResendVerificationView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = 'auth_email'

    def post(self, request):
        emails.send_verification_email(request.user)
        return Response({'detail': 'Verification email sent.'})


class PasswordResetRequestView(_AuthEmailView):
    def post(self, request):
        email = (request.data.get('email') or '').strip()
        if email:
            for user in User.objects.filter(email__iexact=email, is_active=True):
                emails.send_password_reset_email(user)
        # Same answer whether or not the address exists, so this cannot be used to probe accounts.
        return Response({'detail': 'If that email has an account, a reset link is on its way.'})


class PasswordResetConfirmView(_AuthEmailView):
    def post(self, request):
        user = emails.user_from_uid(request.data.get('uid', ''))
        if user is None or not default_token_generator.check_token(user, request.data.get('token', '')):
            return Response({'detail': 'This reset link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        password = validate_password(request.data.get('password') or '')
        user.set_password(password)
        user.save(update_fields=['password'])
        return Response({'detail': 'Password changed.'})
