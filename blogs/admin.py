from django.contrib import admin
from .models import Category, Tag, Blog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display    = ['title', 'author', 'category', 'status', 'views', 'read_time', 'created_at']
    list_filter     = ['status', 'category', 'created_at']
    search_fields   = ['title', 'content', 'author__email', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields   = ['author']
    filter_horizontal = ['tags']
    readonly_fields = ['views', 'read_time', 'created_at', 'updated_at']