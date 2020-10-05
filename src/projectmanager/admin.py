from django.contrib import admin
from .models import Client, Project, Module, Task, SubmittedToQATask, TaskHistory

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client_id')
    list_display_links = ('id', 'name', 'client_id')

    ordering = ('id',)
    search_fields = ('name', 'email', 'client_id')
    list_per_page = 30


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'department', 'status', 'department_head_notified', 'assigned_at')
    list_display_links = ('id', 'name')
    list_editable = ('status', 'assigned_at', 'department_head_notified',)

    ordering = ('id',)
    search_fields = ('name', 'client', 'department', 'code')
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'assigned_team', 'project', 'status', 'team_leader_notified',)
    list_display_links = ('id', 'name')
    list_editable = ('status', 'team_leader_notified',)

    ordering = ('id',)
    search_fields = ('name', 'project', 'assigned_team', )
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'assigned_member', 'module', 'status', 'team_member_notified', 'assigned_at')
    list_display_links = ('id', 'name')
    list_editable = ('status', 'team_member_notified')

    ordering = ('id',)
    search_fields = ('name', 'module', 'assigned_member', )
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


class SubmittedToQATaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'status', 'has_bug', 'is_verified')
    list_display_links = ('id', 'task')
    list_editable = ('status', 'has_bug', 'is_verified')

    ordering = ('id',)
    search_fields = ('task',)
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields

class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'module', 'project', 'submitted_task')
    list_display_links = ('id', 'task', 'module', 'project', 'submitted_task')

    ordering = ('id',)
    search_fields = ('task',)
    list_per_page = 30
    readonly_fields = ('created_at', 'modified_at')  # to show read only fields


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubmittedToQATask, SubmittedToQATaskAdmin)
admin.site.register(TaskHistory, TaskHistoryAdmin)
