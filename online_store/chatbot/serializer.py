from rest_framework.serializers import ModelSerializer
from .models import chat, ChatMessage
from google import genai
import os
from online_store.settings.dev import *



client = genai.Client(api_key=genai_key)
chat_model = client.chats.create(model="gemini-2.5-flash")

class chat_serializer(ModelSerializer):
    class Meta:
        model = chat
        fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return chat.objects.create(**validated_data)


class ChatMessage_serializer(ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = ['message', 'response']

    def create(self, validated_data):
        message = validated_data['message']

        chat_pk = self.context["view"].kwargs.get("chat_pk")

        chat_object = chat.objects.get(pk=chat_pk)
        response = chat_model.send_message(message)
        validated_data['chat'] = chat_object
        validated_data['response'] = response.text

        return ChatMessage.objects.create(**validated_data)