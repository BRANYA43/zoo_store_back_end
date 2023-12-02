from accounts.models import Profile
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'email', 'is_active', 'is_staff', 'joined')
    search_fields = ('uuid', 'email', 'is_active', 'is_staff', 'joined')
    list_filter = ('uuid', 'email', 'is_active', 'is_staff', 'joined')
    exclude = [
        'groups',
        'user_permissions'
    ]

    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'first_name', 'last_name')
    search_fields = ('uuid', 'user', 'first_name', 'last_name')
    list_filter = ('uuid', 'user', 'first_name', 'last_name')


admin.site.unregister(Group)
