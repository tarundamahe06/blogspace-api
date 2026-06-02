from django.urls import path
from .views import ToggleLikeView, LikeStatusView

urlpatterns = [
    path('<int:blog_id>/',        ToggleLikeView.as_view(),  name='toggle_like'),
    path('<int:blog_id>/status/', LikeStatusView.as_view(),  name='like_status'),
]