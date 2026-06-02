from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender_username  = serializers.CharField(source='sender.username', read_only=True)
    sender_full_name = serializers.SerializerMethodField()
    blog_slug        = serializers.SerializerMethodField()
    blog_title       = serializers.SerializerMethodField()

    class Meta:
        model  = Notification
        fields = [
            'id', 'sender', 'sender_username', 'sender_full_name',
            'notification_type', 'message',
            'blog', 'blog_slug', 'blog_title',
            'comment', 'is_read', 'created_at',
        ]
        read_only_fields = ['sender', 'receiver', 'is_read', 'created_at']

    def get_sender_full_name(self, obj):
        return obj.sender.full_name

    def get_blog_slug(self, obj):
        return obj.blog.slug if obj.blog else None

    def get_blog_title(self, obj):
        return obj.blog.title if obj.blog else None