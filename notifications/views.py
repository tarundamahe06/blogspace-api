from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class   = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            receiver=self.request.user
        ).select_related('sender', 'blog', 'comment')


class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                receiver=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {'detail': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read'})


class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        return Response({'detail': 'All notifications marked as read'})


class UnreadNotificationCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})


class DeleteNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                receiver=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {'detail': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        notification.delete()
        return Response(
            {'detail': 'Notification deleted'},
            status=status.HTTP_204_NO_CONTENT
        )