from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import (
    AboutMeView,
    RegisterView,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view, FooBarView, HelloWorld, UserOrdersListView, UserOrdersDataExport,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),

    path('<int:user_id>/orders/', UserOrdersListView.as_view(), name='user-orders'),
    path('<int:user_id>/orders/export/', UserOrdersDataExport.as_view(), name='user-orders-export'),

    path('register/', RegisterView.as_view(), name='register'),

    path('set-cookie/', set_cookie_view, name='set_cookie'),
    path('get-cookie/', get_cookie_view, name='get_cookie'),

    path('set-session/', set_session_view, name='set_session'),
    path('get-session/', get_session_view, name='get_session'),

    path('foobar/', FooBarView.as_view(), name='foobar'),

    path('hello/', HelloWorld.as_view(), name='hello'),

]
