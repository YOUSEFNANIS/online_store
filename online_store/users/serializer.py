from django.db import transaction
from rest_framework import serializers
from .models import customer, seller, User
from online_store.validator import validate_password


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

    class Meta:
        model = seller
        fields = ['id', 'store_name', 'first_name', 'last_name', 'email', 'password', 
                'balance', 'profile_image', 'phone_number']
        read_only_fields = ['balance']

    def create(self, validated_data):

        first_name = validated_data['user'].pop('first_name')
        last_name = validated_data['user'].pop('last_name')
        email = validated_data['user'].pop('email')
        password = validated_data.pop('password')
        store_name = validated_data.pop('store_name')

        username = f"{first_name.lower()}_{last_name.lower()}"

        with transaction.atomic():
            # 3. Create the User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return seller.objects.create(
                user=user,
                store_name=store_name,
                phone_number=validated_data.get('phone_number', ''),
                profile_image=validated_data.get('profile_image'),
            )

    def update(self, instance, validated_data):
        return _update_with_user(instance, validated_data)

    def validate(self, attrs):
        if hasattr(attrs, 'password'):
            validate_password(attrs)

        return super().validate(attrs)

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
        username = f"{first_name.lower()}_{last_name.lower()}"

        with transaction.atomic():
            # 3. Create the User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return customer.objects.create(
                user=user,
                phone_number=validated_data.get('phone_number', ''),
                profile_image=validated_data.get('profile_image'),
            )

    def update(self, instance, validated_data):
        return _update_with_user(instance, validated_data)

    def validate(self, attrs):
        if hasattr(attrs, 'password'):
            validate_password(attrs)

        return super().validate(attrs)