from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering        = ['-created_at']
    list_display    = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'created_at']
    list_filter     = ['is_staff', 'is_superuser', 'is_active']
    search_fields   = ['email', 'username', 'first_name', 'last_name']

    fieldsets = (
        (None,               {'fields': ('email', 'password')}),
        ('Personal Info',    {'fields': ('username', 'first_name', 'last_name', 'bio')}),
        ('Permissions',      {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates',  {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']