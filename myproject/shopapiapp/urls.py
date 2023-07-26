from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shopapiapp.views import (
    hello_api_view,
    GroupsAPIView,
    GroupListAPIView,
    ProductViewSet, OrderViewSet
)

app_name = 'shopapiapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)


urlpatterns = [
    path('hello/', hello_api_view, name='api-hello'),

    path('group-names/', GroupsAPIView.as_view(), name='api-group-names'),
    path('groups/', GroupListAPIView.as_view(), name='api-groups'),

    path('', include(routers.urls)),
]
