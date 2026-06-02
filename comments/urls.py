from django.urls import path
from .views import (
    CommentListCreateView,
    CommentUpdateDeleteView,
)

urlpatterns = [
    path('<int:blog_id>/',  CommentListCreateView.as_view(),  name='comment_list_create'),
    path('<int:pk>/edit/',  CommentUpdateDeleteView.as_view(), name='comment_update_delete'),
]