from django.db import transaction
from rest_framework import serializers
from .models import customer, seller, User
from online_store.validator import validate_password
from . import emails


def _unique_username(first_name, last_name):
    base = f"{first_name.lower()}_{last_name.lower()}"
    username, n = base, 1
    while User.objects.filter(username=username).exists():
        n += 1
        username = f"{base}{n}"
    return username


def _update_with_user(instance, validated_data):
    user_data = validated_data.pop('user', {})
    password = validated_data.pop('password', None)

    with transaction.atomic():
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        if password:
            user.set_password(password)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
    return instance


class SellerSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    store_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = seller
        fields = ['id', 'store_name', 'first_name', 'last_name', 'email', 'password',
                'balance', 'profile_image', 'store_image', 'phone_number']
        read_only_fields = ['balance']

    def create(self, validated_data):

        first_name = validated_data['user'].pop('first_name')
        last_name = validated_data['user'].pop('last_name')
        email = validated_data['user'].pop('email')
        password = validated_data.pop('password')
        store_name = validated_data.pop('store_name')

        username = _unique_username(first_name, last_name)

        with transaction.atomic():
            # 3. Create the User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            transaction.on_commit(lambda: emails.send_verification_email(user))
            return seller.objects.create(
                user=user,
                store_name=store_name,
                phone_number=validated_data.get('phone_number', ''),
                profile_image=validated_data.get('profile_image'),
                store_image=validated_data.get('store_image'),
            )

    def update(self, instance, validated_data):
        return _update_with_user(instance, validated_data)

    def validate_password(self, value):
        return validate_password(value)

class SellerListSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = seller
        fields = ['id', 'store_name', 'store_image', 'product_count', 'rating_avg', 'rating_count']

    def get_rating_avg(self, obj):
        avg = getattr(obj, 'rating_avg', None)
        return round(avg, 1) if avg is not None else None

class CustomerSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    profile_image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = customer
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'profile_image', 'phone_number']


    def create(self, validated_data):
        first_name = validated_data['user'].pop('first_name')
        last_name = validated_data['user'].pop('last_name')
        email = validated_data['user'].pop('email')
        password = validated_data.pop('password')

        # 2. Generate a unique username
        username = _unique_username(first_name, last_name)

        with transaction.atomic():
            # 3. Create the User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            transaction.on_commit(lambda: emails.send_verification_email(user))
            return customer.objects.create(
                user=user,
                phone_number=validated_data.get('phone_number', ''),
                profile_image=validated_data.get('profile_image'),
            )

    def update(self, instance, validated_data):
        return _update_with_user(instance, validated_data)

    def validate_password(self, value):
        return validate_password(value)