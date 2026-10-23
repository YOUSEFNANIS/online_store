from . import tasks, models, serializer, order_flow, ledger, filters as customFilters
from datetime import timedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.db.models import Avg, Count, F, IntegerField, OuterRef, Prefetch, Q, Subquery, Sum, Value, prefetch_related_objects
from django.db.models.functions import Coalesce, Concat
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from online_store import permissions
from django.core.mail import send_mail
from online_store.pagination import CustomPagination, PrecountedPaginator
from django.core.cache import cache
from asgiref.sync import sync_to_async
from .tasks import send_mail, send_order_message

class SendOrderReceiptView(APIView):
    def post(self, request, *args, **kwargs):
        
        try:
            user_email = request.data.get('email')
            order_number = 1

            if not user_email or not order_number:
                return Response(
                    {"error": "Email and order_number are required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            send_order_message(order_number, user_email)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def product_queryset():
    stats = (models.Review.objects.filter(product=OuterRef('pk')).order_by()
             .values('product').annotate(avg=Avg('rating'), n=Count('id')))
    return (models.product.objects.prefetch_related('images').select_related('seller')
            .annotate(rating_avg=Subquery(stats.values('avg')),
                      rating_count=Coalesce(Subquery(stats.values('n')), 0)))


class ProductViewSet(ModelViewSet):
    serializer_class = serializer.ProductSerialzer
    filter_backends = [filters.SearchFilter, customFilters.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_class = customFilters.ProductFilter
    ordering_fields = ['price', 'id', 'name', 'inventory']
    ordering = ['-id']
    pagination_class = CustomPagination
    permission_classes = [permissions.IsSeller]

    def get_queryset(self):

        user = self.request.user
        queryset = product_queryset()
        if hasattr(user, 'seller'):
            return queryset.filter(seller=user.seller)

        return queryset

    @action(detail=True, methods=['get'], url_path='related')
    def related(self, request, pk=None):
        current = get_object_or_404(models.product, pk=pk)
        in_stock = product_queryset().exclude(pk=current.pk).filter(inventory__gt=0).order_by('-id')
        picked = []
        if current.category_id:
            picked = list(in_stock.filter(category_id=current.category_id)[:8])
        if len(picked) < 8:
            seen = [p.pk for p in picked]
            picked += list(in_stock.filter(seller_id=current.seller_id).exclude(pk__in=seen)[:8 - len(picked)])
        return Response(self.get_serializer(picked, many=True).data)

    def list(self, request, *args, **kwargs):
        cache_key = f"products:{request.get_full_path()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response
    
class OrderViewset(ModelViewSet):
    serializer_class = serializer.OrderSerializer
    filter_backends = [customFilters.DjangoFilterBackend]
    filterset_class = customFilters.OrderFilter
    permission_classes = [IsAuthenticated, permissions.IsOwner]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        # The list page shows a summary row only; history, payment and transitions come from the detail call.
        if self.action == 'list':
            return serializer.OrderListSerializer
        return serializer.OrderSerializer

    def get_owner(self):
        # Role and owner id. Read from the authenticated user, so no extra query.
        return order_flow.owner_of(self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['role'] = self.get_owner()[0]
        return context

    def get_queryset(self):
        role, owner_id = self.get_owner()
        if role is None:
            return models.order.objects.none()

        quantity = (models.order_item.objects.filter(order=OuterRef('pk')).order_by()
                    .values('order').annotate(n=Sum('quantity')).values('n'))
        qs = (models.order.objects.filter(**{f'{role}_id': owner_id})
              .annotate(total_quantity=Coalesce(Subquery(quantity), 0, output_field=IntegerField()))
              .order_by('-creation_date', '-id'))

        # A customer sees the store name, a seller sees the customer name.
        if role == 'customer':
            qs = qs.annotate(store_name=F('seller__store_name'))
        else:
            qs = qs.annotate(customer_name=Concat('customer__user__first_name', Value(' '),
                                                  'customer__user__last_name'))

        summary = ['id', 'location', 'order_status', 'total_value', 'creation_date']
        if self.action == 'list':
            return qs.only(*summary)

        # Detail: IsOwner needs the owner user ids, the serializer needs payment fields and the history.
        return (qs.select_related('seller', 'customer')
                .only(*summary, 'payment_method', 'payment_status',
                      'seller__user_id', 'customer__user_id')
                .prefetch_related('events'))

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.order_status in order_flow.FINAL_STATUSES:
            return Response({'detail': 'order is in the final state'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # order_status is read-only on the serializer, so only the other fields are saved here.
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_status = request.data.get('order_status')
        if new_status and new_status != instance.order_status:
            order_flow.change_status(instance.pk, new_status, request.user)
            # Status, payment and history changed, so reload them.
            instance = self.get_object()

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)

class ImageViewSet(ModelViewSet):
    serializer_class = serializer.ImageSerializer
    permission_classes = [permissions.IsProductOwnerOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        return models.productImage.objects.filter(product_id=self.kwargs['products_pk'])

    def perform_create(self, serializer):
        product = get_object_or_404(models.product, pk=self.kwargs['products_pk'])
        serializer.save(product=product)

class CartViewSet(ModelViewSet):
    serializer_class = serializer.CartSerializer
    permission_classes = [permissions.IsCustomer]
    pagination_class = None

    def get_queryset(self):
        # IsCustomer already ran owner_of, so customer_pk is set and no customer query runs.
        return models.cart.objects.filter(customer_id=order_flow.owner_of(self.request.user)[1])

    def list(self, request, *args, **kwargs):
        # One cart per customer: get_or_create already returns it, so serialize it
        # directly instead of fetching the same row again through get_queryset.
        cart, _ = models.cart.objects.get_or_create(customer_id=order_flow.owner_of(request.user)[1])
        prefetch_related_objects([cart], Prefetch('cart_item_set', queryset=cart_items_queryset()))
        return Response(self.get_serializer([cart], many=True).data)


def cart_items_queryset():
    # product and its images load in bulk, so each item costs no extra query.
    # only(): CartItemSerializer reads product name/price; cart is joined just for IsCartItemOwner.
    return (models.cart_item.objects.select_related('product', 'cart')
            .only('id', 'quantity', 'product', 'cart', 'cart__id', 'cart__customer_id', 'product__id', 'product__name', 'product__price')
            .order_by('pk')
            .prefetch_related(Prefetch('product__images', queryset=models.productImage.objects.order_by('pk'))))


class CartItem(ModelViewSet):
    serializer_class = serializer.CartItemSerializer
    permission_classes = [permissions.IsCartItemOwner, permissions.IsCustomer]
    # No pagination: CartItemSerializer caps a cart at MAX_CART_ITEMS rows, so the full list stays small.
    pagination_class = None

    def get_queryset(self):
        return cart_items_queryset().filter(cart__customer_id=order_flow.owner_of(self.request.user)[1])

class OrderItem(ModelViewSet):
    serializer_class = serializer.OrderItemSerializer
    queryset = models.order_item.objects.all() 

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'customer'):
            customer = models.customer.objects.get(user = user)
            order = models.order.objects.get(customer=customer)
        else :
            seller = models.seller.objects.get(user = user)
            order = models.order.objects.get(seller=seller)

        return models.order_item.objects.filter(order=order)


class ReviewViewSet(ModelViewSet):
    serializer_class = serializer.ReviewSerializer
    permission_classes = [permissions.ReviewPermission]

    def _product(self):
        return get_object_or_404(models.product, pk=self.kwargs['products_pk'])

    def get_queryset(self):
        return models.Review.objects.filter(product_id=self.kwargs['products_pk']).select_related('customer__user')

    def _can_review(self, user, product):
        return models.order_item.objects.filter(
            order__customer__user=user, order__order_status=order_flow.DELIVERED, product=product).exists()

    def perform_create(self, serializer):
        product = self._product()
        customer = self.request.user.customer
        if not self._can_review(self.request.user, product):
            raise PermissionDenied('You can review a product after it has been delivered to you.')
        if models.Review.objects.filter(product=product, customer=customer).exists():
            raise ValidationError({'detail': 'You already reviewed this product.'})
        serializer.save(product=product, customer=customer)

    @action(detail=False, methods=['get'], url_path='mine', permission_classes=[IsAuthenticated])
    def mine(self, request, products_pk=None):
        product = self._product()
        review = models.Review.objects.filter(product=product, customer__user=request.user).first()
        return Response({
            'can_review': hasattr(request.user, 'customer') and review is None and self._can_review(request.user, product),
            'review': serializer.ReviewSerializer(review, context={'request': request}).data if review else None,
        })


class ReportViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = serializer.ReportSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Report.objects.none()

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = serializer.CategorySerializer
    # In-stock count, same rule as the landing page, so menus can hide empty categories.
    queryset = models.Category.objects.annotate(
        product_count=Count('products', filter=Q(products__inventory__gt=0))).order_by('id')
    permission_classes = []
    pagination_class = None


class HomeView(APIView):
    """Everything the public landing page shows, in one cached payload."""
    permission_classes = []
    authentication_classes = []

    CACHE_KEY = 'landing:home'
    SECTIONS = 3
    PER_SECTION = 5

    def get(self, request):
        data = cache.get(self.CACHE_KEY)
        if data is None:
            data = self.build(request)
            cache.set(self.CACHE_KEY, data, timeout=60)
        return Response(data)

    def build(self, request):
        from users.models import seller as seller_model
        from users.serializer import SellerListSerializer
        from users.views import seller_directory_queryset

        in_stock = product_queryset().filter(inventory__gt=0).order_by('-id')
        ctx = {'request': request}

        categories = list(models.Category.objects
                          .annotate(product_count=Count('products', filter=Q(products__inventory__gt=0)))
                          .order_by('id')
                          .values('id', 'slug', 'name_en', 'name_ar', 'product_count'))

        # Terms shoppers actually buy: most-ordered product names over the last 30 days,
        # topped up with the newest in-stock names so a young shop still shows chips.
        since = timezone.now() - timedelta(days=30)
        ordered = (models.order_item.objects.filter(order__creation_date__gte=since, product__inventory__gt=0)
                   .values('product__name').annotate(total=Sum('quantity')).order_by('-total')
                   .values_list('product__name', flat=True)[:6])
        trending = list(ordered)
        for name in in_stock.values_list('name', flat=True)[:30]:
            if len(trending) >= 6:
                break
            if name not in trending:
                trending.append(name)

        sections = []
        for category in sorted(categories, key=lambda c: -c['product_count'])[:self.SECTIONS]:
            picked = list(in_stock.filter(category_id=category['id'])[:self.PER_SECTION])
            if picked:
                sections.append({'category': category['id'],
                                 'products': serializer.ProductSerialzer(picked, many=True, context=ctx).data})

        with_images = list(in_stock.filter(images__isnull=False).distinct()[:8])
        stores = list(seller_directory_queryset().filter(product_count__gt=0).order_by('-product_count', 'store_name')[:8])

        return {
            'stats': {'stores': seller_model.objects.count(), 'products': models.product.objects.count()},
            'categories': categories,
            'trending': trending,
            'sections': sections,
            'hero_products': serializer.ProductSerialzer(with_images, many=True, context=ctx).data,
            'stores': SellerListSerializer(stores, many=True, context=ctx).data,
        }


class WishlistViewSet(GenericViewSet):
    serializer_class = serializer.ProductSerialzer
    permission_classes = [IsAuthenticated, permissions.IsCustomer]
    pagination_class = CustomPagination

    def get_queryset(self):
        return (product_queryset().filter(wishlisted_by__customer=self.request.user.customer)
                .only('name', 'description', 'price', 'inventory', 'category', 'seller', 'seller__store_name')
                .order_by('-wishlisted_by__created', '-id'))

    def list(self, request):
        # count wishlist rows directly: skips the product join and annotations
        paginator = type('WishlistPaginator', (PrecountedPaginator,),
                         {'count_source': models.WishlistItem.objects.filter(customer=request.user.customer)})
        self.paginator.django_paginator_class = paginator
        page = self.paginate_queryset(self.get_queryset())
        return self.get_paginated_response(self.get_serializer(page, many=True).data)

    @action(detail=False, methods=['get'], url_path='ids')
    def ids(self, request):
        ids = models.WishlistItem.objects.filter(customer=request.user.customer).values_list('product_id', flat=True)
        return Response(list(ids))

    def create(self, request):
        product = get_object_or_404(models.product, pk=request.data.get('product'))
        models.WishlistItem.objects.get_or_create(customer=request.user.customer, product=product)
        return Response({'product': product.pk}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        models.WishlistItem.objects.filter(customer=request.user.customer, product_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EarningsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = serializer.LedgerEntrySerializer
    permission_classes = [IsAuthenticated, permissions.IsSellerAccount]
    pagination_class = CustomPagination

    def get_queryset(self):
        return models.LedgerEntry.objects.filter(seller=self.request.user.seller)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        seller = request.user.seller
        today = timezone.localdate()
        # Payouts run every Monday.
        next_payout = today + timedelta(days=(7 - today.weekday()) % 7 or 7)
        last = seller.payouts.filter(status='paid').first()
        return Response({
            'balance': seller.balance,
            'threshold': settings.PAYOUT_THRESHOLD,
            'commission_rate': settings.COMMISSION_RATE,
            'next_payout': next_payout,
            'last_payout': {'amount': last.amount, 'paid_at': last.paid_at} if last else None,
        })
