from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleLatestFeed

app_name = 'blogapp'


urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', ArticleLatestFeed(), name='articles-latest'),
]
