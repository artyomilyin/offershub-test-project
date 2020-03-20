from django.db import models
from app.asana_api import AsanaAPI


class WithAPI:
    def __init__(self):
        self.api = AsanaAPI()


class AssigneeManager(models.Manager, WithAPI):
    def all(self):
        users = self.api.get_all_users()
        for row in users:
            model_object = self.model(**row)
            model_object.save()
        return self.get_queryset()


class ProjectManager(models.Manager, WithAPI):
    def all(self):
        projects = self.api.get_all_projects()
        for row in projects:
            model_object = self.model(**row)
            model_object.save()
        return self.get_queryset()


class TaskManager(models.Manager, WithAPI):
    def all(self):
        tasks = self.api.get_all_tasks()
        foreignkey_fields = ['assignee', 'projects']
        for row in tasks:
            object_to_save = {key: value for key, value in row.items() if key not in foreignkey_fields}
            model_object, model_object_created = self.model.objects.get_or_create(**object_to_save)
            if row['assignee']:
                assignee, created = Assignee.objects.get_or_create(**row['assignee'])
                if created:
                    assignee.save()
                model_object.assignee = assignee
            model_object.save(from_django=False)
            if row['projects']:
                model_object.projects.clear()
                for project in row['projects']:
                    project, created = Project.objects.get_or_create(**project)
                    if created:
                        project.save()
                    model_object.projects.add(project)
            model_object.save(from_django=False)
        return self.get_queryset()


class Assignee(models.Model, WithAPI):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=250)
    
    objects = AssigneeManager()

    def __str__(self):
        return f'Assignee: {self.name}'


class Project(models.Model, WithAPI):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=250)

    objects = ProjectManager()

    def __str__(self):
        return f'Project: {self.name}'


class Task(models.Model, WithAPI):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=1000)
    notes = models.TextField()
    assignee = models.ForeignKey(to=Assignee, on_delete=models.CASCADE, null=True)
    projects = models.ManyToManyField(Project)

    objects = TaskManager()

    def __str__(self):
        return f'Task: {self.name}'

    def save(self, from_django=True, *args, **kwargs):
        if from_django:
            update_fields = ['name', 'notes']
            update_object = {key: value for key, value in self.__dict__.items() if key in update_fields}
            print("TASK:UPDATE:")
            projects = self.projects
            print(update_object)
            print(projects)
            self.api.client.tasks.update_task(self.gid, params=update_object)
        super(Task, self).save(*args, **kwargs)
