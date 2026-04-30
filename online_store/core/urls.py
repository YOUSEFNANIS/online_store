from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path
from rest_framework_nested.routers import NestedSimpleRouter

router = SimpleRouter()

router.register('cart', views.Cart, basename='cart')
cart_router = NestedSimpleRouter(router, r'cart', lookup='cart')
cart_router.register('cartitem', views.CartItem, basename='cart-item')

router.register('orders', views.OrderViewset, basename='orders')
order_router = NestedSimpleRouter(router, r'orders', lookup='orders')
order_router.register('orderitem', views.OrderItem, basename='order-item')

router.register('products', views.ProductViewSet, basename='product')
product_router = NestedSimpleRouter(router, r'products', lookup='products')
product_router.register('images', views.ImaegViewset, basename='product-images')
urlpatterns = [path('mail/', views.SendOrderReceiptView.as_view(), name='send-email')]
urlpatterns += router.urls + cart_router.urls + order_router.urls + product_router.urls