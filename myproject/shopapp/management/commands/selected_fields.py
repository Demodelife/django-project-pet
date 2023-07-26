from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start select fields')

        product_fields = Product.objects.values('pk', 'name')
        user_infos = User.objects.values_list('pk', 'username')

        for p_values in product_fields:
            print(p_values)

        print(40 * '-')

        for u_info in user_infos:
            print(u_info)

        print(40 * '-')

        user_infos = User.objects.values_list('username', flat=True)

        for u_info in user_infos:
            print(u_info)

        product_fields = Product.objects.only('pk')
        for p_values in product_fields:
            print(p_values)

        self.stdout.write(self.style.SUCCESS('Done!'))