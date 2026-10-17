from rest_framework import serializers
from core.models import product
from . import models


class MessageProductSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = product
        fields = ['id', 'name', 'price', 'first_image']

    def get_first_image(self, obj):
        image = obj.images.first()
        if not image:
            return None
        request = self.context.get('request')
        url = image.image.url
        return request.build_absolute_uri(url) if request else url


class MessageSerializer(serializers.ModelSerializer):
    mine = serializers.SerializerMethodField()
    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all(), required=False, allow_null=True, write_only=True)
    product_info = MessageProductSerializer(source='product', read_only=True)

    class Meta:
        model = models.Message
        fields = ['id', 'body', 'mine', 'is_read', 'creation_date', 'product', 'product_info']
        read_only_fields = ['id', 'is_read', 'creation_date']

    def get_mine(self, obj):
        return obj.sender_id == self.context['request'].user.id

    def validate_body(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Message cannot be empty.')
        return value


class ConversationSerializer(serializers.ModelSerializer):
    # other_name is the counterpart: store name for customers, customer name for sellers.
    other_name = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Conversation
        fields = ['id', 'other_name', 'last_message', 'last_message_at', 'unread_count']

    def get_other_name(self, obj):
        if self.context['request'].user.id == obj.seller.user_id:
            user = obj.customer.user
            return f'{user.first_name} {user.last_name}'.strip() or user.username
        return obj.seller.store_name

    def get_last_message(self, obj):
        # last_body is annotated in the view to avoid N+1 queries
        body = getattr(obj, 'last_body', None)
        return body[:120] if body else None
