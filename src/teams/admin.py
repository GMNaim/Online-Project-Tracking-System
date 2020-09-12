from django.contrib import admin
from .models import Team, Membership
# Register your models here.


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'is_member', 'is_leader')
    list_display_links = ('id', 'user', )
    list_editable = ('is_member', 'is_leader')
    search_fields = ('id', 'user', 'team', 'is_member', 'is_leader')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'department')


admin.site.register(Team, TeamAdmin)
admin.site.register(Membership, MembershipAdmin)
