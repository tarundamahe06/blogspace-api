from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bookmark
from blogs.models import Blog
from blogs.serializers import BlogListSerializer
from notifications.models import Notification


class ToggleBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response(
                {'detail': 'Blog not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            blog=blog
        )

        if not created:
            bookmark.delete()
            return Response({
                'message':       'Bookmark removed',
                'is_bookmarked': False,
            })

        # Notify blog author of bookmark
        if request.user != blog.author:
            Notification.objects.create(
                receiver          = blog.author,
                sender            = request.user,
                notification_type = 'BOOKMARK',
                message           = f'{request.user.username} bookmarked your blog "{blog.title}"',
                blog              = blog,
            )

        return Response({
            'message':       'Blog bookmarked',
            'is_bookmarked': True,
        }, status=status.HTTP_201_CREATED)


class BookmarkListView(generics.ListAPIView):
    serializer_class   = BlogListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(
            bookmarks__user=self.request.user
        ).select_related('author', 'category').prefetch_related('tags').order_by('-bookmarks__created_at')