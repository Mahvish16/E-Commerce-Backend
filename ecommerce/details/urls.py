from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static 
from .views import RegisterView,LoginView,CategoryView,ProductsView, ProductsImagesView, OrderItemView, BulkOrderItemView, AddressesView,CartItemView,OrderView,LogoutView, RequestPasswordReset, ResetPassword
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('password_reset/confirm/<token>/', ResetPassword.as_view(), name='password'),
    path('categories/', CategoryView.as_view(), name='category'),
    path('products/', ProductsView.as_view(), name='product-list-by-category'),
    path('products/<int:product_id>/images', ProductsImagesView.as_view(), name='product_images'),
    path('orders/',OrderView.as_view(),name="order"),
    path('orders/items/', OrderItemView.as_view(), name='orderitem'),
    path('orders/items/<int:order_id>/', OrderItemView.as_view(), name='orderitem'),
    path('orders/items/bulk/', BulkOrderItemView.as_view(), name='bulkorderitem'),
    path('addresses/', AddressesView.as_view(), name='addresses'),
    path('addresses/<int:pk>/',AddressesView.as_view(), name = 'addresses'),
    path('cart-items/', CartItemView.as_view(), name='cartitem'),
    path('cart-items/<int:pk>/', CartItemView.as_view(), name='cart-item-detail'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

