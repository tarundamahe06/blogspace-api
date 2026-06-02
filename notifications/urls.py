from django.urls import path
from .views import (
    NotificationListView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
    UnreadNotificationCountView,
    DeleteNotificationView,
)

urlpatterns = [
    path('',                          NotificationListView.as_view(),         name='notification_list'),
    path('unread-count/',             UnreadNotificationCountView.as_view(),   name='unread_count'),
    path('mark-all-read/',            MarkAllNotificationsReadView.as_view(),  name='mark_all_read'),
    path('<int:notification_id>/read/',   MarkNotificationReadView.as_view(),  name='mark_read'),
    path('<int:notification_id>/delete/', DeleteNotificationView.as_view(),    name='delete_notification'),
]