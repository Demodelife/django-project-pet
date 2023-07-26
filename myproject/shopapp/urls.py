from django.contrib import admin
from django.urls import path
from shopapp.views import (
    ProductDetailView,
    ShopIndexView,
    GroupListView,
    ProductListView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    ProductCreateView, ProductUpdateView, ProductDeleteView, ProductArchiveView,
)

app_name = 'shopapp'


urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/confirm-delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:pk>/confirm-archive/', ProductArchiveView.as_view(), name='product-archive'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
]
