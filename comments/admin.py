from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'blog', 'parent', 'is_edited', 'created_at']
    list_filter   = ['is_edited', 'created_at']
    search_fields = ['content', 'user__email', 'user__username', 'blog__title']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields   = ['user', 'blog', 'parent']