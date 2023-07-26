from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start bulk actions')

        # info = [
        #     ('Smartphone 1', 200),
        #     ('Smartphone 2', 300),
        #     ('Smartphone 3', 600),
        # ]
        #
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        #
        # for obj in result:
        #     print(obj)

        products = Product.objects.filter(
            name__contains='Smartphone'
        ).update(
            description='This is smartphone'
        )
        print(products)

        self.stdout.write(self.style.SUCCESS('Done!'))