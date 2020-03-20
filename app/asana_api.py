import requests
from django.conf import settings

import asana


class AsanaAPI:

    def __init__(self):
        self.client = asana.Client.access_token(settings.ASANA_TOKEN)

    def get_all_projects(self):
        """ It is possible that this function may return duplicates if
        the same projects appears in several workspaces. To be examined.
        """
        opt_fields = ['gid', 'name']
        workspaces = self.client.workspaces.get_workspaces()
        projects = []
        for workspace in workspaces:
            projects.extend(self.client.projects.get_projects(workspace=workspace['gid'], 
                                                              opt_fields=opt_fields))
        return projects

    def get_project(self, project_id):
        opt_fields = ['gid', 'name']
        return self.client.projects.get_project(project_id, opt_fields=opt_fields)

    def get_tasks_for_project(self, project_id):
        opt_fields = ['gid', 'name', 'notes', 'assignee.gid']
        tasks_for_project = self.client.tasks.get_tasks_for_project(project_id, opt_fields=opt_fields)
        tasks = []
        for task in tasks_for_project:
            flattened_task = dict(task)
            if task['assignee']:
                flattened_task['assignee'] = task['assignee']['gid']
            tasks.append(flattened_task)
        return tasks

    def get_all_tasks(self):
        tasks = []
        for project in self.get_all_projects():
            tasks.extend(self.get_tasks_for_project(project['gid']))
        return tasks

    def get_task(self, task_id):
        opt_fields = ['gid', 'name', 'notes', 'assignee.gid']
        return self.client.tasks.get_task(task_id, opt_fields=opt_fields)
