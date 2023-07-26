from django.test import TestCase
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('accounts:get_cookie'))
        self.assertContains(response, 'cookie')


class FooBarViewTestCase(TestCase):
    def test_foobar_view(self):
        response = self.client.get(reverse('accounts:foobar'))
        expected_data = {
            'foo': 'bar',
            'spam': 'eggs',
        }
        self.assertJSONEqual(response.content, expected_data)
