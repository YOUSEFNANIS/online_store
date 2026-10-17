from django.db import transaction
from django.db.models import Count, Max, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import product
from . import models, serializer

DEFAULT_PAGE = 30
MAX_PAGE = 100


class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = serializer.ConversationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        # No role probe: a user matches only the side of the pair they own (no extra queries).
        qs = models.Conversation.objects.filter(Q(seller__user=user) | Q(customer__user=user))

        last_body = models.Message.objects.filter(conversation=OuterRef('pk')).order_by('-id').values('body')[:1]
        unread = models.Message.objects.filter(
            conversation=OuterRef('pk'), is_read=False).exclude(sender=user).order_by().values('conversation').annotate(
            c=Count('id')).values('c')
        # Load only what ConversationSerializer reads, not whole user/profile rows.
        return qs.select_related('customer__user', 'seller').only(
            'last_message_at',
            'customer__user__first_name', 'customer__user__last_name', 'customer__user__username',
            'seller__store_name', 'seller__user',
        ).annotate(
            last_body=Subquery(last_body),
            unread_count=Coalesce(Subquery(unread), 0),
        )

    def create(self, request):
        # Customer starts (or reuses) a thread with the product's seller and sends the first message.
        if not hasattr(request.user, 'customer'):
            return Response({'detail': 'Only customers can contact sellers.'}, status=status.HTTP_403_FORBIDDEN)

        product_obj = get_object_or_404(product.objects.select_related('seller'), id=request.data.get('product'))
        msg = serializer.MessageSerializer(
            data={'body': request.data.get('body', ''), 'product': product_obj.id},
            context=self.get_serializer_context())
        msg.is_valid(raise_exception=True)

        with transaction.atomic():
            conversation, _ = models.Conversation.objects.get_or_create(
                customer=request.user.customer, seller=product_obj.seller)
            msg.save(conversation=conversation, sender=request.user)
            conversation.last_message_at = timezone.now()
            conversation.save(update_fields=['last_message_at'])

        return Response({'id': conversation.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], url_path='messages')
    def messages(self, request, pk=None):
        conversation = self.get_object()

        if request.method == 'POST':
            msg = serializer.MessageSerializer(data=request.data, context=self.get_serializer_context())
            msg.is_valid(raise_exception=True)
            with transaction.atomic():
                msg.save(conversation=conversation, sender=request.user)
                conversation.last_message_at = timezone.now()
                conversation.save(update_fields=['last_message_at'])
            return Response(msg.data, status=status.HTTP_201_CREATED)

        # Opening the thread marks the counterpart's messages as read.
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

        # Cursor pagination by id: ?before=<id> loads older, ?after=<id> loads only new (poll).
        try:
            limit = min(max(int(request.query_params.get('limit', DEFAULT_PAGE)), 1), MAX_PAGE)
            before = request.query_params.get('before')
            after = request.query_params.get('after')
            before = int(before) if before else None
            after = int(after) if after else None
        except ValueError:
            return Response({'detail': 'Invalid pagination parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        base = conversation.messages.select_related('product').prefetch_related('product__images')
        has_more = False
        if after is not None:
            items = list(base.filter(id__gt=after).order_by('id')[:MAX_PAGE])
        else:
            if before is not None:
                base = base.filter(id__lt=before)
            items = list(base.order_by('-id')[:limit + 1])
            has_more = len(items) > limit
            items = items[:limit][::-1]

        # Poll fetches skip already-loaded messages, so send the read watermark for own ticks.
        read_upto = conversation.messages.filter(sender=request.user, is_read=True).aggregate(m=Max('id'))['m']
        data = serializer.MessageSerializer(items, many=True, context=self.get_serializer_context()).data
        return Response({'results': data, 'has_more': has_more, 'read_upto': read_upto})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        count = models.Message.objects.filter(is_read=False).exclude(sender=request.user).filter(
            Q(conversation__seller__user=request.user) | Q(conversation__customer__user=request.user)).count()
        return Response({'unread': count})
