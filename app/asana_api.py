import requests
from django.conf import settings

import asana




class AsanaAPI:
    TASK_FIELDS = ['gid', 'name', 'notes', 'assignee.gid', 'assignee.name', 'projects.gid', 'projects.name']
    PROJECT_FIELDS = ['gid', 'name']
    USER_FIELDS = ['gid', 'name']

    def __init__(self):
        self.client = asana.Client.access_token(settings.ASANA_TOKEN)

    def get_all_projects(self):
        opt_fields = self.PROJECT_FIELDS
        workspaces = self.client.workspaces.get_workspaces()
        projects = []
        for workspace in workspaces:
            projects.extend(self.client.projects.get_projects(workspace=workspace['gid'], 
                                                              opt_fields=opt_fields))
        return projects

    def get_project(self, project_id):
        opt_fields = self.PROJECT_FIELDS
        return self.client.projects.get_project(project_id, opt_fields=opt_fields)

    def get_tasks_for_project(self, project_id):
        opt_fields = self.TASK_FIELDS
        tasks_for_project = self.client.tasks.get_tasks_for_project(project_id, opt_fields=opt_fields)
        tasks = []
        for task in tasks_for_project:
            tasks.append(task)
        return tasks

    def get_all_tasks(self):
        tasks = []
        for project in self.get_all_projects():
            tasks.extend(self.get_tasks_for_project(project['gid']))
        return tasks

    def get_task(self, task_id):
        opt_fields = self.TASK_FIELDS
        return self.client.tasks.get_task(task_id, opt_fields=opt_fields)

    def get_all_users(self):
        opt_fields = self.USER_FIELDS
        workspaces = self.client.workspaces.get_workspaces()
        users = []
        for workspace in workspaces:
            users.extend(self.client.users.get_users(workspace=workspace['gid'],
                                                     opt_fields=opt_fields))
        return users
