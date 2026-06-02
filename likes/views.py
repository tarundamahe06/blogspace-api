from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Like
from blogs.models import Blog
from notifications.models import Notification


class ToggleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response(
                {'detail': 'Blog not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(
            user=request.user,
            blog=blog
        )

        if not created:
            like.delete()
            return Response({
                'message':     'Blog unliked',
                'likes_count': blog.likes.count(),
            })

        # Create notification only if liker is not the blog author
        if request.user != blog.author:
            Notification.objects.create(
                receiver          = blog.author,
                sender            = request.user,
                notification_type = 'LIKE',
                message           = f'{request.user.username} liked your blog "{blog.title}"',
                blog              = blog,
            )

        return Response({
            'message':     'Blog liked',
            'likes_count': blog.likes.count(),
        }, status=status.HTTP_201_CREATED)


class LikeStatusView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response(
                {'detail': 'Blog not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        likes_count = blog.likes.count()
        is_liked    = False

        if request.user.is_authenticated:
            is_liked = blog.likes.filter(user=request.user).exists()

        return Response({
            'likes_count': likes_count,
            'is_liked':    is_liked,
        })