from django.contrib import admin
from blogapp.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'body', 'published_at'
