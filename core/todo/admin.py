from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    """class to edit admin site for task model"""

    date_hierarchy = "created_date"
    list_display = ["user", "title", "completed", "created_date"]
    list_filter = ["user", "completed"]
    search_fields = ["title"]


admin.site.register(Task, TaskAdmin)
