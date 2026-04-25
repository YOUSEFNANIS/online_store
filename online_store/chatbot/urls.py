from django.urls import path
from . import views
from .views import ChatMessageviewset, Chatviewset
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

router = SimpleRouter()

router.register('chat', Chatviewset)
chat_router = NestedSimpleRouter(router, r'chat', lookup='chat')
chat_router.register('message', ChatMessageviewset, basename='chat_message')

urlpatterns = router.urls + chat_router.urls
