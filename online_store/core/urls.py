from rest_framework.routers import SimpleRouter
from . import views, seller_tools
from django.urls import path
from rest_framework_nested.routers import NestedSimpleRouter

router = SimpleRouter()

router.register('cart', views.CartViewSet, basename='cart')
cart_router = NestedSimpleRouter(router, r'cart', lookup='cart')
cart_router.register('cartitem', views.CartItem, basename='cart-item')

router.register('orders', views.OrderViewset, basename='orders')
order_router = NestedSimpleRouter(router, r'orders', lookup='orders')
order_router.register('orderitem', views.OrderItem, basename='order-item')

router.register('products', views.ProductViewSet, basename='product')
product_router = NestedSimpleRouter(router, r'products', lookup='products')
product_router.register('images', views.ImageViewSet, basename='product-images')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
router.register('reports', views.ReportViewSet, basename='reports')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('wishlist', views.WishlistViewSet, basename='wishlist')
router.register('earnings', views.EarningsViewSet, basename='earnings')
urlpatterns = [
    path('mail/', views.SendOrderReceiptView.as_view(), name='send-email'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('seller/stats/', seller_tools.SellerStatsView.as_view(), name='seller-stats'),
    path('seller/export/orders/', seller_tools.ExportOrdersView.as_view(), name='export-orders'),
    path('seller/export/earnings/', seller_tools.ExportEarningsView.as_view(), name='export-earnings'),
    path('seller/import/products/', seller_tools.ProductImportView.as_view(), name='import-products'),
]
urlpatterns += router.urls + cart_router.urls + order_router.urls + product_router.urls