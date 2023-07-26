from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _, ngettext
from django.views import View
from django.views.generic import TemplateView, CreateView
from accounts.models import Profile


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


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    response = request.COOKIES.get('foo', 'default')
    return HttpResponse(f'Get cookie for key "foo" - {response}')


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
