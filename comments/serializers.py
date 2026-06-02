from rest_framework import serializers
from .models import Comment


class ReplySerializer(serializers.ModelSerializer):
    user_username  = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model  = Comment
        fields = [
            'id', 'user', 'user_username', 'user_full_name',
            'content', 'is_edited', 'created_at', 'updated_at',
        ]

    def get_user_full_name(self, obj):
        return obj.user.full_name


class CommentSerializer(serializers.ModelSerializer):
    user_username  = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    replies        = ReplySerializer(many=True, read_only=True)
    replies_count  = serializers.SerializerMethodField()

    class Meta:
        model  = Comment
        fields = [
            'id', 'user', 'user_username', 'user_full_name',
            'blog', 'parent', 'content', 'is_edited',
            'replies', 'replies_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['user', 'is_edited']

    def get_user_full_name(self, obj):
        return obj.user.full_name

    def get_replies_count(self, obj):
        return obj.replies.count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = ['id', 'blog', 'parent', 'content']

    def validate_content(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError('Comment cannot be empty')
        return value

    def validate(self, attrs):
        # Make sure parent comment belongs to the same blog
        parent = attrs.get('parent')
        blog   = attrs.get('blog')
        if parent and parent.blog != blog:
            raise serializers.ValidationError(
                {'parent': 'Parent comment does not belong to this blog'}
            )
        # Make sure parent is not itself a reply (only one level deep)
        if parent and parent.parent is not None:
            raise serializers.ValidationError(
                {'parent': 'Cannot reply to a reply'}
            )
        return attrs


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = ['content']

    def validate_content(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError('Comment cannot be empty')
        return value

    def update(self, instance, validated_data):
        instance.content   = validated_data.get('content', instance.content)
        instance.is_edited = True
        instance.save()
        return instance