from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',              admin.site.urls),
    path('api/accounts/',       include('accounts.urls')),
    path('api/blogs/',      include('blogs.urls')),
    path('api/comments/',   include('comments.urls')),
    path('api/likes/',      include('likes.urls')),
    path('api/bookmarks/',   include('bookmarks.urls')),
    path('api/follows/',    include('follows.urls')),
    path('api/notifications/',      include('notifications.urls')),
]