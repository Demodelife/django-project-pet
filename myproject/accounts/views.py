from random import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _, ngettext
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, CreateView, ListView
from accounts.models import Profile
from shopapp.models import Order


class AboutMeView(TemplateView):
    template_name = 'accounts/about-me.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register_form.html'
    success_url = reverse_lazy('accounts:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(self.request, user=user)

        return response


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie successfully set!')
    response.set_cookie('foo', 'bar', max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    response = request.COOKIES.get('foo', 'default')
    return HttpResponse(f'Get cookie for key "foo" - {response} + {random()}')


@permission_required('accounts:view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['spam'] = 'eggs'
    return HttpResponse('Session successfully set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    response = request.session.get('spam')
    return HttpResponse(f'Get session for key "spam" - {response}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(
            {
                'foo': 'bar',
                'spam': 'eggs',
            }
        )


class HelloWorld(View):

    welcome_message = _('Hello World')

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items', 0)
        items = int(items_str)
        product_line = ngettext(
            'one product',
            '{count} products',
            items,
        ).format(count=items)
        # product_line = product_line.format()

        return HttpResponse(f'<h1>{self.welcome_message}!</h1>'
                            f'\n<h3>{product_line}</h3>')


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/user-order-list.html'
    context_object_name = 'orders'
    model = Order

    def get_queryset(self):
        user = self.request.user.pk
        queryset = Order.objects.filter(user=user).order_by('pk')
        return queryset

    def get(self, request, *args, **kwargs):
        if kwargs['user_id'] != self.request.user.pk:
            return HttpResponseRedirect(
                reverse(
                    'accounts:user-orders', kwargs={'user_id': self.request.user.id}
                )
            )
        return super().get(request, *args, **kwargs)


class UserOrdersDataExport(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        if self.request.user.id:
            cache_key = self.request.user.id
            orders_data = cache.get(cache_key)
            if orders_data is None:
                orders = Order.objects.filter(user=self.request.user.id)
                orders_data = [
                    {
                        'delivery_address': order.delivery_address,
                        'promocode': order.promocode,
                        'created_at': order.created_at,
                        'products': [(product.name, product.price) for product in order.products.all()]
                    }
                    for order in orders
                ]
                cache.set(cache_key, orders_data, 100)
            return JsonResponse({'orders': orders_data})
        return JsonResponse({'detail': 'User not found'}, status=404)