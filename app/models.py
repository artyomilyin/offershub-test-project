from django.db import models
from app.asana_api import AsanaAPI


class APIManager(models.Manager):
    def __init__(self):
        self.api = AsanaAPI()


class AssigneeManager(APIManager):
    def all(self):
        users = self.api.get_all_users()
        for row in users:
            model_object = self.model(**row)
            model_object.save()
        return self.get_queryset()


class ProjectManager(models.Manager):
    def all(self):
        projects = self.api.get_all_projects()
        for row in projects:
            model_object = self.model(**row)
            model_object.save()
        return self.get_queryset()


class TaskManager(models.Manager):
    def all(self):
        tasks = self.api.get_all_tasks()
        for row in tasks:
            object_to_save = {key: value for key, value in row.items() if key not in ['assignee']}
            model_object = self.model(**object_to_save)
            if row['assignee']:
                assignee = Assignee(**row['assignee'])
                assignee.save()
                model_object.assignee = assignee
            model_object.save()
        return self.get_queryset()


class Assignee(models.Model):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=250)
    
    objects = AssigneeManager()

    def __str__(self):
        return f'Assignee: {self.name}'


class Project(models.Model):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=250)

    objects = ProjectManager()

    def __str__(self):
        return f'Project: {self.name}'


class Task(models.Model):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=1000)
    notes = models.TextField()
    assignee = models.ForeignKey(to=Assignee, on_delete=models.CASCADE, null=True)
    projects = models.CharField(max_length=2500)

    objects = TaskManager()

    def __str__(self):
        return f'Task: {self.name}'
