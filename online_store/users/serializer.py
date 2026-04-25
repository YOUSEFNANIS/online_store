from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import customer, seller, User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.db import transaction
import re

class seller_serializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile_image = serializers.ImageField()

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
            return seller.objects.create(user=user, store_name=store_name)
    
    def validate_password(self, data):
        password = '' + data['password']
        if len(password) < 8:
            raise serializers.ValidationError('password is too short')
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError('Password must contain at least upper case character')
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError('Password must contain at least 1 character')
        if not re.search(r"[0-9]", password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return data
    def validate(self, attrs):
        print(attrs)
        if hasattr(attrs, 'password'):
            self.validate_password(attrs)

        return super().validate(attrs)

class customer_serializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    profile_image = serializers.ImageField()
    
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
            return customer.objects.create(user=user)
    
    def validate_password(self, data):
        password = data['password']
        if len(password) < 8:
            raise serializers.ValidationError('password is too short')
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError('Password must contain at least upper case character')
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError('Password must contain at least 1 character')
        if not re.search(r"[0-9]", password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return data
    def validate(self, attrs):
        if hasattr(attrs, 'password'):
            self.validate_password(attrs)

        return super().validate(attrs)