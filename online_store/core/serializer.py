from . import models
from rest_framework import serializers
from django.db import transaction

class image_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.productImage
        fields = ['image', 'product']


class product_serialzer(serializers.ModelSerializer):
    images = image_serializer(many=True, read_only=True)
    id = serializers.UUIDField(read_only=True)
    store_name = serializers.CharField(source='seller.store_name')
    class Meta:
        model = models.product
        fields = ['id', 'description', 'price', 'images', 'name', 'inventory', 'store_name']

    def create(self, validated_data):
        
        user = self.context['request'].user
        seller = models.seller.objects.get(user=user)
        validated_data['seller'] = seller
        return models.product.objects.create(**validated_data)

class order_serializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer', read_only=True)
    store_name = serializers.CharField(source='seller.store_name', read_only=True)
    id = serializers.UUIDField(read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)
    creation_date = serializers.DateTimeField(format="%Y %b %d, %H:%M", read_only=True)
    class Meta:
        model = models.order
        fields = ['id', 'location', 'order_status', 'total_value', 'customer_name', 'store_name', 'creation_date', 'total_quantity']

    def get_total_quantity(self, obj):
        # Returns the sum of all 'quantity' fields in the items
        from django.db.models import Sum
        result = obj.order_item_set.aggregate(total=Sum('quantity'))['total']
        return result or 0
    
    @transaction.atomic
    def create(self, validated_data):
                
        user = self.context['request'].user
        customer = models.customer.objects.get(user=user)
        validated_data['customer'] = customer
        
        
        cart_object = models.cart.objects.get(customer = customer)
        cartitems = models.cart_item.objects.filter(cart=cart_object)
        validated_data['total_value'] = sum(
                        item.product.price * item.quantity
                        for item in cartitems
                    )
    
        validated_data['seller'] = cartitems[0].product.seller
        order_object = models.order.objects.create(**validated_data)

        items = [models.order_item(order= order_object,
                                    product = item.product,
                                    quantity = item.quantity
                                    ) for item in cartitems]

        models.order_item.objects.bulk_create(items)
        cart_object.delete()
        return order_object


    def validate(self, data):
        
        if self.context['request'].method !='POST':
            request = self.context.get('request')
            user = request.user

            if hasattr(user, 'customer') and hasattr(data, 'order_status'):
                modified_data = {'order_status': data['order_status']}
                return modified_data
        
        return data
    
    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        if hasattr(user, 'seller'):
            fields['order_status'].read_only = True

        if hasattr(user, 'customer'):
            fields['total_value'].read_only = True
        return fields

class orderItem_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.order_item
        fields = ['product', 'quantity']


class cartItem_serializer(serializers.ModelSerializer):
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    first_image = serializers.SerializerMethodField()
    price = serializers.DecimalField(source='product.price', max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = models.cart_item
        fields = [
            'id',          # cart item id
            'cart',        # cart id
            'product',
            'price',     # product id (used for POST)
            'product_name',
            'first_image',
            'quantity'
        ]

    def get_first_image(self, obj):
        image = obj.product.images.first()
        if image:
            return image.image.url
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        customer = models.customer.objects.get(user = user)
        cart = models.cart.objects.get(customer = customer)
        product = validated_data['product']
        cart_item = models.cart_item.objects.filter(cart=cart, product=product).first()
        if cart_item != None:
            cart_item.quantity +=1
            cart_item.save()
            return cart_item
        return models.cart_item.objects.create(**validated_data)
    
class cart_serializer(serializers.ModelSerializer): 
    
    cart_item_set = cartItem_serializer(many=True, read_only=True)
    class Meta:
        model = models.cart
        fields = ['id', 'cart_item_set']

    def create(self, validated_data):
        cart_id = self.context['view'].kwargs['cart_pk']
        cart = models.cart.objects.get(id=cart_id)

        validated_data['cart'] = cart

        return models.cart_item.objects.create(**validated_data)
