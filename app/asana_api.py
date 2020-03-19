import requests
from django.conf import settings


PROJECTS_PATH = '/projects'
TASKS_PATH = '/tasks'
API_BASE = 'https://app.asana.com/api/1.0'
API_HEADERS = {'Authorization': f'Bearer {settings.ASANA_TOKEN}'}


class AsanaAPI:
    api_base = API_BASE
    headers = API_HEADERS

    def __init__(self, ModelName):
        self.model = ModelName

    def _get_request(self, path, **kwargs):
        return requests.get(f'{self.api_base}{path}', headers=self.headers, **kwargs).json()['data']

    def get_all_projects(self):
        params = {'opt_fields':'gid,name'}
        return self._get_request(PROJECTS_PATH, params=params)

    def get_project(self, project_id):
        params = {'opt_fields':'gid,name'}
        return self._get_request(f'{PROJECTS_PATH}/{project_id}', params=params)

    def get_tasks_for_project(self, project_id):
        params = {'opt_fields':'gid,name,notes,assignee.gid'}
        middle = self._get_request(f'{PROJECTS_PATH}/{project_id}{TASKS_PATH}', params=params)
        dct = []
        for task in middle:
            formatted_task = dict(task)
            if task['assignee']:
                formatted_task['assignee'] = task['assignee']['gid']
            dct.append(formatted_task)
        return dct

    def get_all_tasks(self):
        tasks = []
        for project in self.get_all_projects():
            tasks.extend(self.get_tasks_for_project(project['gid']))
        return tasks

    def get_task(self, task_id):
        params = {'opt_fields':'gid,name,notes,assignee.gid'}
        return self._get_request(f'{PROJECTS_PATH}/{project_id}', params=params)
