from django.urls import path
from .views import (
    BlogListCreateView,
    BlogDetailView,
    CategoryListView,
    CategoryDetailView,
    TagListView,
    TagDetailView,
    FeedView,
    TrendingView,
    UserBlogsView,
    SearchView,
    CreateCategoryView,
    CreateTagView,
)

urlpatterns = [
    # Blogs
    path('',             BlogListCreateView.as_view(), name='blog_list_create'),

    # These must come BEFORE <slug:slug>/
    path('feed/',        FeedView.as_view(),           name='feed'),
    path('trending/',    TrendingView.as_view(),        name='trending'),
    path('search/',      SearchView.as_view(),          name='search'),

    # Categories
    path('categories/',             CategoryListView.as_view(),   name='category_list'),
    path('categories/create/',      CreateCategoryView.as_view(), name='category_create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),

    # Tags
    path('tags/',             TagListView.as_view(),   name='tag_list'),
    path('tags/create/',      CreateTagView.as_view(), name='tag_create'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag_detail'),

    # User blogs
    path('user/<str:username>/', UserBlogsView.as_view(), name='user_blogs'),

    # Slug must always be LAST
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]