from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "status",
        "priority",
        "assigned_to",
        "project",
        "due_date",
    )
    search_fields = ("title",)


admin.site.register(Task, TaskAdmin)