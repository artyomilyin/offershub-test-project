from django.db import models
from app.asana_api import AsanaAPI


class ProjectManager(models.Manager):
    def all(self):
        api = AsanaAPI(Project)
        projects = api.get_all_projects()
        for row in projects:
            model_object = self.model(**row)
            model_object.save()
        return self.get_queryset()


class Project(models.Model):
    gid = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)
    objects = ProjectManager()

    def __str__(self):
        return f'Project: {self.name}'


class TaskManager(models.Manager):
    def all(self):
        api = AsanaAPI(Task)
        tasks = api.get_all_tasks()
        for row in tasks:
            model_object = self.model(**row)
            model_object.save()
        return self.get_queryset()


class Task(models.Model):
    gid = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)
    notes = models.TextField()
    assignee = models.CharField(max_length=250, null=True)
    objects = TaskManager()

    def __str__(self):
        return f'Task: {self.name}'
