from . import tasks, models, serializer, filters as customFilters
from django.db import transaction
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from online_store import permissions
from django.core.mail import send_mail
from online_store.pagination import CustomPagination
from django.core.cache import cache
from asgiref.sync import sync_to_async
from .tasks import send_mail, send_order_message

class SendOrderReceiptView(APIView):
    def post(self, request, *args, **kwargs):
        
        try:
            user_email = request.data.get('email')
            order_number = 1

            if not user_email or not order_number:
                return Response(
                    {"error": "Email and order_number are required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            send_order_message(order_number, user_email)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductViewSet(ModelViewSet):
    serializer_class = serializer.ProductSerialzer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = CustomPagination
    permission_classes = [permissions.IsSeller]

    def get_queryset(self):

        user = self.request.user
        queryset =  models.product.objects.prefetch_related('images').select_related('seller')
        if hasattr(user, 'seller'):
            return queryset.filter(seller=user.seller)

        return queryset

    def list(self, request, *args, **kwargs):
        cache_key = f"products:{request.get_full_path()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response
    
class OrderViewset(ModelViewSet):
    serializer_class = serializer.OrderSerializer
    filter_backends = [customFilters.DjangoFilterBackend]
    filterset_class = customFilters.OrderFilter
    permission_classes = [permissions.IsOwner]
    pagination_class = CustomPagination
    def get_queryset(self):
        
        if hasattr(self.request.user, 'seller'):
            seller = models.seller.objects.get(user = self.request.user)
            return models.order.objects.filter(seller = seller)
        
        else:
            customer = models.customer.objects.get(user = self.request.user)
            return models.order.objects.filter(customer = customer)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.order_status in ['completed', 'cancelled']:
            return Response({'detail': 'order is in the final state'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                    
    
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if hasattr(request.user, 'seller'):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if hasattr(serializer.validated_data, 'order_status')==False:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if instance.order_status == 'pending' and serializer.validated_data['order_status'] == 'completed':
            self.addBalance(instance)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def addBalance(self, order):
        order.seller.balance += order.total_value
        tasks.message_seller.delay(order.id, order.seller.user.email)
        #order.seller.save()

class ImageViewset(ModelViewSet):
    serializer_class = serializer.ImageSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['products_pk']
        product_object = models.product.objects.get(id = product_id)
        return models.productImage.objects.filter(product = product_object)
    
    def perform_create(self, serializer):
        product_id = self.kwargs['products_pk']
        product = models.product.objects.get(id=product_id)
        serializer.save(product=product)

class CartViewSet(ModelViewSet):
    serializer_class = serializer.cart_serializer
    permission_classes = [permissions.IsCustomer]

    def get_queryset(self):
        user = self.request.user
        customer = models.customer.objects.get(user=user)
        return models.cart.objects.get_or_create(customer=customer)
    
class CartItem(ModelViewSet):
    serializer_class = serializer.CartItemSerializer
    permission_classes = [permissions.IsCartItemOwner, permissions.IsCustomer]
    
    def get_queryset(self):
        user = self.request.user
        customer = models.customer.objects.get(user = user)
        cart = models.cart.objects.get(customer=customer)
        return models.cart_item.objects.filter(cart=cart)

class OrderItem(ModelViewSet):
    serializer_class = serializer.OrderItemSerializer
    queryset = models.order_item.objects.all() 

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'customer'):
            customer = models.customer.objects.get(user = user)
            order = models.order.objects.get(customer=customer)
        else :
            seller = models.seller.objects.get(user = user)
            order = models.order.objects.get(seller=seller)

        return models.order_item.objects.filter(order=order)