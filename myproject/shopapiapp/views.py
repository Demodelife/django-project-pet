from csv import DictWriter
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from shopapiapp.serializers import GroupSerializer, ProductSerializer, OrderSerializer
from shopapp.common import save_csv_products, save_csv_orders
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
    queryset = Product.objects.order_by('pk').all()
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

    @method_decorator(cache_page(60))
    def list(self, *args, **kwargs):
        print('--before cache---')
        return super().list(*args, **kwargs)

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

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'archived',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(
        methods=['post'],
        detail=False,
        parser_classes=[MultiPartParser],
    )
    def upload_csv(self, request: Request) -> Response:
        products = save_csv_products(
            file=request.FILES['file'].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    """
    Order View set.
    """
    queryset = Order.objects.order_by('pk').all()
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

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request) -> HttpResponse:
        response = HttpResponse(content_type='text/csv')
        filename = 'orders-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'delivery_address',
            'promocode',
            'created_at',
            'user',
            'products',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for order in queryset:
            products = order.products.all()
            writer.writerow({
                field: getattr(order, field) if field != 'products'
                else [product.name for product in products]
                for field in fields
            })

        return response

    @action(
        methods=['post'],
        detail=False,
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self, request: Request) -> Response:
        orders = save_csv_orders(
            file=request.FILES['file'].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
