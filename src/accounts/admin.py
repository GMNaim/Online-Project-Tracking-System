from django.contrib import admin
from .models import Role, User


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'id')
    ordering = ('id',)

class UserAdmin(admin.ModelAdmin):
    fields = (
        'first_name', 'middle_name', 'last_name', 'gender', 'username', 'email', 'password', 'mobile_number',
        'address', 'department', 'role', 'profile_picture', 'groups', 'user_permissions', 'date_joined', 'last_login', 'is_active',
        'is_superuser', 'is_staff')
    list_display = ('id', 'username', 'email', 'role', 'department',)
    list_display_links = ('id', 'username',)
    ordering = ('id',)
    search_fields = ('username', 'email', 'role__name', 'department__name', 'gender')
    list_per_page = 30


admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
