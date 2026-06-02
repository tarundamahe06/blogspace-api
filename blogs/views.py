from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Blog, Category, Tag


from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer

from .serializers import (
    BlogListSerializer,
    BlogDetailSerializer,
    BlogCreateUpdateSerializer,
    CategorySerializer,
    TagSerializer,
)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class CategoryListView(generics.ListAPIView):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field       = 'slug'


class TagListView(generics.ListAPIView):
    queryset           = Tag.objects.all()
    serializer_class   = TagSerializer
    permission_classes = [permissions.AllowAny]


class TagDetailView(generics.RetrieveAPIView):
    queryset           = Tag.objects.all()
    serializer_class   = TagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field       = 'slug'


class BlogListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['status', 'category', 'author']
    search_fields      = ['title', 'content', 'excerpt', 'tags__name']
    ordering_fields    = ['created_at', 'views', 'likes_count']
    ordering           = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Authenticated users see their own drafts + all published
        if user.is_authenticated:
            return Blog.objects.filter(
                Q(status='published') | Q(author=user)
            ).select_related('author', 'category').prefetch_related('tags')

        # Anonymous users see published only
        return Blog.objects.filter(
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogCreateUpdateSerializer
        return BlogListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog = serializer.save(author=request.user)
        return Response(
            BlogDetailSerializer(blog, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field       = 'slug'

    def get_queryset(self):
        return Blog.objects.select_related(
            'author', 'category'
        ).prefetch_related('tags')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BlogCreateUpdateSerializer
        return BlogDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        instance   = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        blog = serializer.save()
        return Response(
            BlogDetailSerializer(blog, context={'request': request}).data
        )


class FeedView(generics.ListAPIView):
    serializer_class   = BlogListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            following_ids = user.following.values_list('following_id', flat=True)
        except Exception:
            following_ids = []
        return Blog.objects.filter(
            author__in=following_ids,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')


class TrendingView(generics.ListAPIView):
    serializer_class   = BlogListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        from django.utils import timezone
        from datetime import timedelta
        last_7_days = timezone.now() - timedelta(days=7)
        return Blog.objects.filter(
            status='published',
            created_at__gte=last_7_days
        ).select_related('author', 'category').prefetch_related('tags').order_by('-views')


class UserBlogsView(generics.ListAPIView):
    serializer_class   = BlogListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Blog.objects.filter(
            author__username=username,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')
    



class SearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({
                'blogs': [],
                'users': [],
                'tags':  [],
            })

        User = get_user_model()

        blogs = Blog.objects.filter(
            Q(title__icontains=query)    |
            Q(content__icontains=query)  |
            Q(excerpt__icontains=query)  |
            Q(tags__name__icontains=query),
            status='published'
        ).distinct().select_related('author', 'category').prefetch_related('tags')[:10]

        users = User.objects.filter(
            Q(username__icontains=query)   |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )[:5]

        tags = Tag.objects.filter(
            name__icontains=query
        )[:5]

        return Response({
            'blogs': BlogListSerializer(blogs, many=True, context={'request': request}).data,
            'users': UserSerializer(users, many=True).data,
            'tags':  TagSerializer(tags,  many=True).data,
        })
    






class CreateCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        name = request.data.get('name', '').strip()
        if not name:
            return Response(
                {'detail': 'Name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(name) < 2:
            return Response(
                {'detail': 'Name must be at least 2 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        category, created = Category.objects.get_or_create(
            name__iexact=name,
            defaults={'name': name}
        )
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class CreateTagView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        name = request.data.get('name', '').strip().lower()
        if not name:
            return Response(
                {'detail': 'Name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(name) < 2:
            return Response(
                {'detail': 'Name must be at least 2 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tag, created = Tag.objects.get_or_create(
            name__iexact=name,
            defaults={'name': name}
        )
        return Response(
            TagSerializer(tag).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )