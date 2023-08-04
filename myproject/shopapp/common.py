from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User

from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)
    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding
    )
    reader = DictReader(csv_file)
    products = Product.objects.filter(name__contains='smartphone')
    orders = [
        Order(**row, user=User.objects.get(id=1))
        for row in reader
    ]

    Order.objects.bulk_create(orders)

    for order in orders:
        order.products.set(products)

    return orders
