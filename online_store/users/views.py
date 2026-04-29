from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializer import customer_serializer, seller_serializer
from rest_framework.decorators import action
from .models import seller, customer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import get_user_model
from online_store.online_store.permissions import IsOwnerOrAdmin

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
                path= '/'  # Helps with CSRF
            )
            
        if refresh_token:
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
        print(response.data['access'])
        print(response.data['refresh'])

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
                secure=False,  # True in production
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
        user = request.user
        if hasattr(user, 'customer'):
            user_object = customer.objects.get(user = request.user)
            id = getattr(user_object, 'id', "Default Value")
            url = user_object.profile_image.url if user_object.profile_image else None
            return Response({
            "id": id,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone_number": getattr(user_object, 'phone_number', None),
            'profile_image': url,
            })
        
        elif hasattr(user, 'seller'):
            user_object = seller.objects.get(user = request.user)
            id = getattr(user_object, 'id', "Default Value")
            url = user_object.profile_image.url if user_object.profile_image else None
            return Response({
                "id": id,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "balance": getattr(user_object, 'balance', None),
                "phone_number": getattr(user_object, 'phone_number', None),
                'profile_image': url,
            })
    
class customer_viewset(ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = customer.objects.all()
    serializer_class = customer_serializer

class seller_viewset(ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = seller.objects.all()
    serializer_class = seller_serializer