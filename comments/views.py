from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Comment
from .serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
)
from notifications.models import Notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('blog_id')
        return Comment.objects.filter(
            blog_id=blog_id,
            parent=None
        ).select_related('user').prefetch_related('replies__user')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(user=request.user)

        # Notify blog author of new comment
        if request.user != comment.blog.author:
            Notification.objects.create(
                receiver          = comment.blog.author,
                sender            = request.user,
                notification_type = 'COMMENT',
                message           = f'{request.user.username} commented on your blog "{comment.blog.title}"',
                blog              = comment.blog,
                comment           = comment,
            )

        # Notify parent comment owner of reply
        if comment.parent and request.user != comment.parent.user:
            Notification.objects.create(
                receiver          = comment.parent.user,
                sender            = request.user,
                notification_type = 'REPLY',
                message           = f'{request.user.username} replied to your comment on "{comment.blog.title}"',
                blog              = comment.blog,
                comment           = comment,
            )

        return Response(
            CommentSerializer(comment, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset           = Comment.objects.select_related('user')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentUpdateSerializer
        return CommentSerializer

    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        instance   = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(
            CommentSerializer(comment, context={'request': request}).data
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied('You can only delete your own comments')
        instance.delete()
        return Response(
            {'detail': 'Comment deleted'},
            status=status.HTTP_204_NO_CONTENT
        )