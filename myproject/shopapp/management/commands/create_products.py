import random
import string
import random
from django.core.management import BaseCommand
from shopapp.models import Product


def random_str(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Create products...')
        for _ in range(100):
            Product.objects.get_or_create(
                name=random_str(random.randint(3, 20)),
                description=random_str(random.randint(20, 99)),
                price=round(random.uniform(0, 1000), 2)
            )
        self.stdout.write(self.style.SUCCESS('Products created'))