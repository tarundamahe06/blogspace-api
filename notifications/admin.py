from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display    = ['sender', 'receiver', 'notification_type', 'is_read', 'created_at']
    list_filter     = ['notification_type', 'is_read', 'created_at']
    search_fields   = ['sender__email', 'sender__username', 'receiver__email', 'receiver__username', 'message']
    raw_id_fields   = ['sender', 'receiver', 'blog', 'comment']
    readonly_fields = ['created_at']