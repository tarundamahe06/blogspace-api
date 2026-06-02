from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name        = serializers.SerializerMethodField()
    followers_count  = serializers.SerializerMethodField()
    following_count  = serializers.SerializerMethodField()
    blogs_count      = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'bio', 'followers_count', 'following_count',
            'blogs_count', 'created_at',
        ]

    def get_full_name(self, obj):
        return obj.full_name

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_blogs_count(self, obj):
        return obj.blogs.filter(status='published').count()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'bio']

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError('Username already taken')
        return value