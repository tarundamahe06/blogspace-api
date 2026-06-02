from django.db import models
from django.conf import settings


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('LIKE',     'Like'),
        ('COMMENT',  'Comment'),
        ('REPLY',    'Reply'),
        ('FOLLOW',   'Follow'),
        ('BOOKMARK', 'Bookmark'),
    ]

    receiver          = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender            = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message           = models.CharField(max_length=255)
    blog              = models.ForeignKey(
        'blogs.Blog',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='notifications'
    )
    comment           = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='notifications'
    )
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender.username} → {self.receiver.username} ({self.notification_type})'
