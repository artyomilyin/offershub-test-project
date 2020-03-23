from django.contrib import admin
from .models import Project, Task, Assignee


class ApiModelAdmin(admin.ModelAdmin):
    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all()


@admin.register(Project)
class ProjectAdmin(ApiModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(ApiModelAdmin):
    list_display = ['name', 'assignee']

    def save_related(self, request, form, formsets, change):
        """Save every new project and delete each old project
        """
        new_projects = [project.gid for project in form.cleaned_data['projects']]
        old_projects = [project.gid for project in form.instance.projects.all()]
        to_add = [project for project in new_projects if project not in old_projects]
        to_del = [project for project in old_projects if project not in new_projects]
        print(f"to_add: {to_add}")
        print(f"to_del: {to_del}")
        for project_gid in to_add:
            update_object = {'project': project_gid}
            form.instance.api.client.tasks.add_project_for_task(form.instance.gid, params=update_object)
        for project_gid in to_del:
            update_object = {'project': project_gid}
            form.instance.api.client.tasks.remove_project_for_task(form.instance.gid, params=update_object)

        return super(TaskAdmin, self).save_related(request, form, formsets, change)


@admin.register(Assignee)
class AssigneeAdmin(ApiModelAdmin):
    pass
