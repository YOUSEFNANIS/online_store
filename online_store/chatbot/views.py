import os
from .models import chat, ChatMessage
from .serializer import chat_serializer, ChatMessage_serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

class Chatviewset(ModelViewSet):
    serializer_class = chat_serializer
    queryset = chat.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({"chat_id": instance.id},
                        status=status.HTTP_201_CREATED
        )

class ChatMessageviewset(ModelViewSet):
    serializer_class = ChatMessage_serializer
    queryset = ChatMessage.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        return Response({"chat_id": instance.id},
                        status=status.HTTP_201_CREATED
        )