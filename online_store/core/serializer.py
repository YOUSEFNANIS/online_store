from . import models, order_flow
from django.db import transaction
from django.db.models import F
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.productImage
        fields = ['id', 'image', 'product']
        read_only_fields = ['product']


class ProductSerialzer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    store_name = serializers.CharField(source='seller.store_name', read_only=True)
    seller_id = serializers.IntegerField(read_only=True)
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = models.product
        fields = ['id', 'description', 'price', 'images', 'name', 'inventory', 'store_name', 'seller_id',
                  'rating_avg', 'rating_count', 'category']

    # rating_* are annotated by the view; missing on a freshly created product.
    def get_rating_avg(self, obj):
        avg = getattr(obj, 'rating_avg', None)
        return round(avg, 1) if avg is not None else None

    def get_rating_count(self, obj):
        return getattr(obj, 'rating_count', 0)

    def create(self, validated_data):
        
        user = self.context['request'].user
        seller = models.seller.objects.get(user=user)
        validated_data['seller'] = seller
        return models.product.objects.create(**validated_data)

class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer', read_only=True)
    store_name = serializers.CharField(source='seller.store_name', read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)
    creation_date = serializers.DateTimeField(format="%Y %b %d, %H:%M", read_only=True)
    allowed_transitions = serializers.SerializerMethodField(read_only=True)
    status_history = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.order
        fields = ['id', 'location', 'order_status', 'total_value', 'customer_name', 'store_name', 'creation_date',
                  'total_quantity', 'allowed_transitions', 'status_history', 'payment_method', 'payment_status']
        # Status changes go through order_flow.change_status, never a plain field write.
        read_only_fields = ['order_status', 'payment_method', 'payment_status']

    def get_total_quantity(self, obj):
        # Returns the sum of all 'quantity' fields in the items
        from django.db.models import Sum
        result = obj.order_item_set.aggregate(total=Sum('quantity'))['total']
        return result or 0

    def get_allowed_transitions(self, obj):
        role = order_flow.role_of(self.context['request'].user)
        return order_flow.allowed_transitions(role, obj.order_status)

    def get_status_history(self, obj):
        return [{'status': e.status, 'by': e.actor_role, 'at': e.created.isoformat()} for e in obj.events.all()]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        customer = models.customer.objects.get(user=user)
        validated_data['customer'] = customer
        validated_data.pop('total_value', None)

        cart_object = models.cart.objects.get(customer=customer)
        cart_items = list(models.cart_item.objects.filter(cart=cart_object))
        if not cart_items:
            raise serializers.ValidationError({'detail': 'Your cart is empty.'})

        # Lock the products so two checkouts cannot both take the last unit.
        products = {p.id: p for p in models.product.objects
                    .select_for_update().select_related('seller').filter(id__in=[i.product_id for i in cart_items])}
        for item in cart_items:
            product = products[item.product_id]
            if product.inventory < item.quantity:
                raise serializers.ValidationError({'detail': f'Not enough stock for {product.name}.'})

        # One order per seller, so every seller is paid only for their own products.
        by_seller = {}
        for item in cart_items:
            by_seller.setdefault(products[item.product_id].seller, []).append(item)

        orders = []
        for seller, items in by_seller.items():
            order_object = models.order.objects.create(
                seller=seller,
                total_value=sum(products[i.product_id].price * i.quantity for i in items),
                **validated_data)
            models.order_item.objects.bulk_create([
                models.order_item(order=order_object, product=products[i.product_id], quantity=i.quantity)
                for i in items])
            for i in items:
                models.product.objects.filter(pk=i.product_id).update(inventory=F('inventory') - i.quantity)
            models.OrderStatusEvent.objects.create(order=order_object, status=order_flow.PENDING, actor_role='customer')
            order_flow.notify(order_object, user, f'New order #{order_object.id}.')
            orders.append(order_object)

        cart_object.delete()
        return orders[0]

    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        if hasattr(user, 'customer'):
            fields['total_value'].read_only = True
        return fields

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.order_item
        fields = ['product', 'quantity']


class CartItemSerializer(serializers.ModelSerializer):
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    first_image = serializers.SerializerMethodField()
    price = serializers.DecimalField(source='product.price', max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = models.cart_item
        fields = [
            'id', 
            'cart',
            'product',
            'price',
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
    
class CartSerializer(serializers.ModelSerializer): 
    
    cart_item_set = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = models.cart
        fields = ['id', 'cart_item_set']

    def create(self, validated_data):
        cart_id = self.context['view'].kwargs['cart_pk']
        cart = models.cart.objects.get(id=cart_id)

        validated_data['cart'] = cart

        return models.cart_item.objects.create(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    mine = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = ['id', 'rating', 'text', 'created', 'customer_name', 'mine']
        read_only_fields = ['created']

    def get_customer_name(self, obj):
        user = obj.customer.user
        last = f' {user.last_name[:1]}.' if user.last_name else ''
        return f'{user.first_name}{last}'.strip() or user.username

    def get_mine(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.customer.user_id == user.id

    def validate_text(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError('Review is too long (max 1000 characters).')
        return value.strip()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ['id', 'product', 'seller', 'reason', 'details']

    def validate_details(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError('Details are too long (max 1000 characters).')
        return value.strip()

    def validate(self, attrs):
        product, seller = attrs.get('product'), attrs.get('seller')
        if bool(product) == bool(seller):
            raise serializers.ValidationError('Report either a product or a seller.')
        user = self.context['request'].user
        target_seller = product.seller if product else seller
        if target_seller.user_id == user.id:
            raise serializers.ValidationError('You cannot report your own store.')
        already = models.Report.objects.filter(reporter=user, status='open', product=product, seller=seller)
        if already.exists():
            raise serializers.ValidationError('You already reported this. We are reviewing it.')
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'slug', 'name_en', 'name_ar']


class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LedgerEntry
        fields = ['id', 'kind', 'amount', 'order', 'created']
