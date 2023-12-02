from accounts.models import Profile
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ('uuid', 'first_name', 'last_name')
    readonly_fields = ('uuid',)
    can_delete = False
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'email', 'is_active', 'is_staff', 'joined')
    search_fields = ('uuid', 'email', 'is_active', 'is_staff', 'joined')
    list_filter = ('is_active', 'is_staff', 'joined')
    exclude = [
        'groups',
        'user_permissions'
    ]

    fields = ('uuid', 'email', 'is_active', 'is_staff', 'last_login', 'joined')
    readonly_fields = ('uuid', 'is_active', 'last_login', 'joined')

    inlines = [ProfileInline]


admin.site.unregister(Group)
