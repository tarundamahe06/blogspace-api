from django.db import models
from django.conf import settings


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    blog = models.ForeignKey(
        'blogs.Blog',
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')
        ordering        = ['-created_at']

    def __str__(self):
        return f'{self.user.username} bookmarked {self.blog.title}'