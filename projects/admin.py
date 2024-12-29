from django.contrib import admin
from projects.models import Project, ProjectMember


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "owner"
    )
    search_fields = ("name",)


class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "user",
        "role"
    )
    search_fields = ("project",)


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
