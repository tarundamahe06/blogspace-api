from django.urls import path
from .views import ToggleBookmarkView, BookmarkListView

urlpatterns = [
    path('',              BookmarkListView.as_view(),   name='bookmark_list'),
    path('<int:blog_id>/', ToggleBookmarkView.as_view(), name='toggle_bookmark'),
]