from django.contrib import admin
from .models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display    = ['follower', 'following', 'created_at']
    list_filter     = ['created_at']
    search_fields   = ['follower__email', 'follower__username', 'following__email', 'following__username']
    raw_id_fields   = ['follower', 'following']
    readonly_fields = ['created_at']