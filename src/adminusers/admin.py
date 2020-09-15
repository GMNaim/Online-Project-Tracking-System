from django.contrib import admin
from .models import Client, Project

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client_id')
    list_display_links = ('id', 'name', 'client_id')

    ordering = ('id',)
    search_fields = ('name', 'email', 'client_id')
    list_per_page = 30


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'department', 'status', 'department_head_notified')
    list_display_links = ('id', 'name')

    ordering = ('id',)
    search_fields = ('name', 'client', 'department', 'code')
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)