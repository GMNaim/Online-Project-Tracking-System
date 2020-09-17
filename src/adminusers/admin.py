from django.contrib import admin
from .models import Client, Project, Module, Task

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client_id')
    list_display_links = ('id', 'name', 'client_id')

    ordering = ('id',)
    search_fields = ('name', 'email', 'client_id')
    list_per_page = 30


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'department', 'status', 'department_head_notified',)
    list_display_links = ('id', 'name')
    list_editable = ('status', )

    ordering = ('id',)
    search_fields = ('name', 'client', 'department', 'code')
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'assigned_team', 'project', 'status', 'team_leader_notified',)
    list_display_links = ('id', 'name')
    list_editable = ('status', )

    ordering = ('id',)
    search_fields = ('name', 'project', 'assigned_team', )
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'assigned_member', 'module', 'status', 'team_member_notified', 'assigned_at')
    list_display_links = ('id', 'name')
    list_editable = ('status', )

    ordering = ('id',)
    search_fields = ('name', 'module', 'assigned_member', )
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Task, TaskAdmin)
