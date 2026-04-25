from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path
from rest_framework_nested.routers import NestedSimpleRouter

router = SimpleRouter()

router.register('cart', views.cart, basename='cart')
cart_router = NestedSimpleRouter(router, r'cart', lookup='cart')
cart_router.register('cartitem', views.cartItem, basename='cart-item')

router.register('orders', views.orderViewset, basename='orders')
order_router = NestedSimpleRouter(router, r'orders', lookup='orders')
order_router.register('orderitem', views.orderItem, basename='order-item')

router.register('products', views.productViewset, basename='product')
product_router = NestedSimpleRouter(router, r'products', lookup='products')
product_router.register('images', views.imaegViewset, basename='product-images')
urlpatterns = [path('mail/', views.SendOrderReceiptView.as_view(), name='send-email')]
urlpatterns += router.urls + cart_router.urls + order_router.urls + product_router.urls