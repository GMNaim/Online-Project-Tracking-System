from django.contrib import admin
from .models import Department


class DepartmentAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'is_active')
    list_display = ('id', 'name', 'is_active')
    list_display_links = ('id', 'name',)
    ordering = ('id',)
    search_fields = ('name', )
    list_per_page = 30


admin.site.register(Department, DepartmentAdmin)

