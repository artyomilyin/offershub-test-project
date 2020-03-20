from django.contrib import admin
from .models import Project, Task


class ApiModelAdmin(admin.ModelAdmin):
    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all()


@admin.register(Project)
class ProjectAdmin(ApiModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(ApiModelAdmin):
    pass
