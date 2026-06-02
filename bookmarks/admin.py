from django.contrib import admin
from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display    = ['user', 'blog', 'created_at']
    list_filter     = ['created_at']
    search_fields   = ['user__email', 'user__username', 'blog__title']
    raw_id_fields   = ['user', 'blog']
    readonly_fields = ['created_at']