from django.urls import path
from .views import (
    ToggleFollowView,
    FollowStatusView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    path('<int:user_id>/',           ToggleFollowView.as_view(),  name='toggle_follow'),
    path('<int:user_id>/status/',    FollowStatusView.as_view(),  name='follow_status'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='followers_list'),
    path('<int:user_id>/following/', FollowingListView.as_view(), name='following_list'),
]