from rest_framework import serializers
from .models import Blog, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    blogs_count = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'description', 'blogs_count']

    def get_blogs_count(self, obj):
        return obj.blogs.filter(status='published').count()


class TagSerializer(serializers.ModelSerializer):
    blogs_count = serializers.SerializerMethodField()

    class Meta:
        model  = Tag
        fields = ['id', 'name', 'slug', 'blogs_count']

    def get_blogs_count(self, obj):
        return obj.blogs.filter(status='published').count()


class BlogListSerializer(serializers.ModelSerializer):
    author_username  = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    category_name    = serializers.CharField(source='category.name', read_only=True)
    tags             = TagSerializer(many=True, read_only=True)
    likes_count      = serializers.SerializerMethodField()
    comments_count   = serializers.SerializerMethodField()
    is_liked         = serializers.SerializerMethodField()
    is_bookmarked    = serializers.SerializerMethodField()

    class Meta:
        model  = Blog
        fields = [
            'id', 'title', 'slug', 'excerpt', 'status',
            'author', 'author_username', 'author_full_name',
            'category', 'category_name', 'tags',
            'likes_count', 'comments_count', 'is_liked', 'is_bookmarked',
            'views', 'read_time', 'created_at', 'updated_at',
        ]

    def get_author_full_name(self, obj):
        return obj.author.full_name

    def get_likes_count(self, obj):
        try:
            return obj.likes.count()
        except Exception:
            return 0

    def get_comments_count(self, obj):
        try:
            return obj.comments.count()
        except Exception:
            return 0

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                return obj.likes.filter(user=request.user).exists()
            except Exception:
                return False
        return False

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                return obj.bookmarks.filter(user=request.user).exists()
            except Exception:
                return False
        return False


class BlogDetailSerializer(BlogListSerializer):
    class Meta(BlogListSerializer.Meta):
        fields = BlogListSerializer.Meta.fields + ['content']


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model  = Blog
        fields = ['title', 'content', 'excerpt', 'status', 'category', 'tags']

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('Title must be at least 5 characters')
        return value

    def validate_content(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError('Content must be at least 20 characters')
        return value