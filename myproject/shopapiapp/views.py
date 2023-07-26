from django.contrib.auth.models import Group
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from shopapiapp.serializers import GroupSerializer, ProductSerializer, OrderSerializer
from shopapp.models import Product, Order


@api_view()
def hello_api_view(request: Request) -> Response:
    """
    Simple API View function. Returns message 'Hello World!'.
    """

    return Response({'message': 'Hello World!'})


class GroupsAPIView(APIView):
    """
    Groups API View. Returns group names list.
    """

    def get(self, request: Request) -> Response:
        groups = Group.objects.all()
        group_names = [grp.name for grp in groups]

        return Response({'groups': group_names})


class GroupListAPIView(ListCreateAPIView):
    """
    Group list API View. Returns group list.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@extend_schema(description='Products views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Product View set.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        'name',
        'description',
    ]
    filterset_fields = [
        'name',
        'description',
        'price',
        'archived',
    ]
    ordering_fields = [
        'name',
        'description',
        'price',
    ]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieve **product**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class OrderViewSet(ModelViewSet):
    """
    Order View set.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    search_fields = [
        'delivery_address',
        'promocode',
    ]
    filterset_fields = [
        'delivery_address',
        'promocode',
    ]
    ordering_fields = [
        'created_at',
        'promocode',
    ]


