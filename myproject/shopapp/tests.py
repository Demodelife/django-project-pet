from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from myproject.settings import LOGIN_URL
from shopapp.models import Product


class ProductCreateViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_superuser(username='admin-test', password='adminTEST45123')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_product_create(self):

        self.client.login(username='admin-test', password='adminTEST45123')
        response = self.client.post(
            reverse('shopapp:product-create'),
            {
                'name': 'Any',
                'description': 'ANYdescription',
                'price': '123.12',

            }
        )

        self.assertRedirects(response, reverse('shopapp:product-list'))
        self.assertTrue(User.objects.filter(id=self.user.id).exists())


class ProductDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.product = Product.objects.create(name='TestProduct')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()

    def test_product_detail(self):
        response = self.client.get(
            reverse('shopapp:product-detail', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_product_detail_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product-detail', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_product_list(self):
        response = self.client.get(reverse('shopapp:product-list'))
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).order_by('id').all(),
            values=map(lambda p: p.pk, response.context['products']),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/product-list.html')


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Admin_test', password='test123')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_order_list(self):
        response = self.client.get(reverse('shopapp:order-list'))
        self.assertEqual(response.status_code, 200)

    def test_order_list_for_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:order-list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(LOGIN_URL), response.url)