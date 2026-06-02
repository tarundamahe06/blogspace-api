from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Follow
from accounts.serializers import UserSerializer
from notifications.models import Notification

User = get_user_model()


class ToggleFollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user_to_follow == request.user:
            return Response(
                {'detail': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()
            return Response({
                'message':         'User unfollowed',
                'is_following':    False,
                'followers_count': user_to_follow.followers.count(),
            })

        # Create notification
        Notification.objects.create(
            receiver          = user_to_follow,
            sender            = request.user,
            notification_type = 'FOLLOW',
            message           = f'{request.user.username} started following you',
        )

        return Response({
            'message':         'User followed',
            'is_following':    True,
            'followers_count': user_to_follow.followers.count(),
        }, status=status.HTTP_201_CREATED)


class FollowStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

        return Response({
            'is_following':    is_following,
            'followers_count': user.followers.count(),
            'following_count': user.following.count(),
        })


class FollowersListView(generics.ListAPIView):
    serializer_class   = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.filter(following__following_id=user_id)


class FollowingListView(generics.ListAPIView):
    serializer_class   = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.filter(followers__follower_id=user_id)