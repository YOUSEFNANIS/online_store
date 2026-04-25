from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, response
from . import serializer
from . import models
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from users.permissions import IsSeller, IsCustomer, IsOwner
from . import filters as customFilters
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.views import APIView
from .tasks import message_seller
from online_store.pagination import CustomPagination
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

            # 1. Construct the email
            subject = f"Your Receipt for Order #{order_number}"
            message = f"Thank you for shopping at JR Shop! Your order #{order_number} is confirmed."
            html_message = f"<h1>Order Confirmed</h1><p>Thank you for your order <strong>#{order_number}</strong>.</p>"
            send_mail(
                subject=subject,
                message=message,
                from_email='nanisyousof@gmail.com',
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
            return Response({"message": "Receipt sent successfully!"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class productViewset(ModelViewSet):
    serializer_class = serializer.product_serialzer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = CustomPagination
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'seller'):
            seller = models.seller.objects.get(user=user)
            return models.product.objects.filter(seller=seller)
        return models.product.objects.all()

class orderViewset(ModelViewSet):
    serializer_class = serializer.order_serializer
    filter_backends = [customFilters.DjangoFilterBackend]
    filterset_class = customFilters.OrderFilter
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
                    raise ValidationError("Cannot modify finalized order")
                    
    
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if hasattr(request.user, 'seller'):
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        if instance.order_status == 'pending' and serializer.validated_data['order_status'] == 'completed':
            self.addBalance(instance)

        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
    def addBalance(self, order):
        order.seller.balance += order.total_value
        message_seller.delay(order.id, order.seller.user.email)
        #order.seller.save()

class imaegViewset(ModelViewSet):
    serializer_class = serializer.image_serializer
    
    def get_queryset(self):
        product_id = self.kwargs['products_pk']
        product_object = models.product.objects.get(id = product_id)
        return models.productImage.objects.filter(product = product_object)
    
    def perform_create(self, serializer):
        product_id = self.kwargs['products_pk']
        product = models.product.objects.get(id=product_id)
        serializer.save(product=product)

class cart(ModelViewSet):
    serializer_class = serializer.cart_serializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        user = self.request.user
        customer = models.customer.objects.get(user=user)
        return models.cart.objects.get_or_create(customer=customer)
    
class cartItem(ModelViewSet):
    serializer_class = serializer.cartItem_serializer
    permission_classes = [IsOwner]
    
    def get_queryset(self):
        user = self.request.user
        customer = models.customer.objects.get(user = user)
        cart = models.cart.objects.get(customer=customer)
        return models.cart_item.objects.filter(cart=cart)

class orderItem(ModelViewSet):
    serializer_class = serializer.orderItem_serializer
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