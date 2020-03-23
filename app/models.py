from django.db import models
from app.asana_api import WithAPI


class AsanaModel(models.Model, WithAPI):
    """This is a base model for all Asana Models. It contains __eq__ method's override as well as 
    overrides for __hash__ and __str__ methods.
    """
    EQ_IGNORED_FIELDS = ['_state', 'api']

    def __eq__(self, other):
        if not other:
            return super(AsanaModel, self).__eq__(other)
        values = [(k,v) for k,v in self.__dict__.items() if k not in self.EQ_IGNORED_FIELDS]
        other_values = [(k,v) for k,v in other.__dict__.items() if k not in self.EQ_IGNORED_FIELDS]
        return values == other_values

    def __hash__(self):
        return super(AsanaModel, self).__hash__()

    def __str__(self):
        return f'{self.__class__.__name__}: {self.name}'

    class Meta:
        abstract = True


class AsanaManager(models.Manager, WithAPI):
    def create_or_update_if_necessary(self, item, model=None):
        """Check if there is an existing model for the item and also check if it contains relevant field values.
        """
        if not model:
            model = self.model
        modified = False
        item_to_compare = model(**item)
        item_gid = item.pop('gid')
        model_object, created = model.objects.get_or_create(gid=item_gid, defaults=item)
        if created or item_to_compare != model_object:
            print(f"{model.__name__}: {item_gid} {item} object didn't exist or differs from existing. Saving...")
            for i in item:
                setattr(model_object, i, item[i])
            model_object.save(from_django_admin=False)
            modified = True
        return model_object, modified


class AssigneeManager(AsanaManager):
    def all(self):
        """Get all the users from Asana and save them if necessary. Delete those which don't exist anymore.
        """
        users = self.api.get_all_users()
        user_gids = [user['gid'] for user in users]
        for user in users:
            self.create_or_update_if_necessary(user)
        self.model.objects.exclude(pk__in=user_gids).delete()
        return self.get_queryset()


class ProjectManager(AsanaManager):
    def all(self):
        """Get all the projects from Asana and save them if necessary. Delete those which don't exist anymore.
        """
        projects = self.api.get_all_projects()
        project_gids = [project['gid'] for project in projects]
        for project in projects:
            self.create_or_update_if_necessary(project)
        self.model.objects.exclude(pk__in=project_gids).delete()
        return self.get_queryset()    


class TaskManager(AsanaManager):
    def all(self):
        """Get all the tasks from Asana (for each project and each workspace) and save them if necessary.
        Delete those which don't exist anymore.
        """
        tasks = self.api.get_all_tasks()
        task_gids = [task['gid'] for task in tasks]
        # these fields will be processed separately
        foreignkey_fields = ['assignee', 'projects']
        for row in tasks:
            initial_dict = {key: value for key, value in row.items() if key not in foreignkey_fields}
            model_object, modified = self.create_or_update_if_necessary(initial_dict)
            if modified:
                model_object.save()
            
            foreignkey_updated = False
            assignee_orig = model_object.assignee
            projects_orig = model_object.projects
            if row['assignee']:
                model_object.assignee, modified = self.create_or_update_if_necessary(row['assignee'], Assignee)
                if modified:
                    model_object.save()
            else:
                model_object.assignee = None
            if row['projects']:
                updated_projects = []
                for project in row['projects']:
                    project_object, _ = self.create_or_update_if_necessary(project, Project)
                    updated_projects.append(project_object)
                if model_object.projects != updated_projects:
                    model_object.projects.set(updated_projects)
            else:
                model_object.projects.clear()

            if assignee_orig != model_object.assignee or projects_orig != model_object.projects:
                model_object.save(from_django_admin=False)
        self.model.objects.exclude(pk__in=task_gids).delete()
        return self.get_queryset()


class Assignee(AsanaModel):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=250)
    
    objects = AssigneeManager()

    def save(self, from_django_admin=False, *args, **kwargs):
        # this override is needed only to handle 'from_django_admin' argument from ancestor
        return super(Assignee, self).save(*args, **kwargs)



class Project(AsanaModel):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=250)

    objects = ProjectManager()
    
    def save(self, from_django_admin=False, *args, **kwargs):
        if not from_django_admin:
            object_to_create = {'name': self.name,
                                'workspace': list(self.api.client.workspaces.get_workspaces())[0]['gid']}
            if self.gid:
                self.api.client.projects.update_project(self.gid, object_to_create)
            else:
                response = self.api.client.projects.create_project(object_to_create)
                self.gid = response['gid']
        print(f"[DB]Project {self.name} saving...")
        return super(Project, self).save(*args, **kwargs)


class Task(AsanaModel):
    gid = models.CharField(max_length=250, primary_key=True, editable=False)
    name = models.CharField(max_length=1000)
    notes = models.TextField(blank=True)
    assignee = models.ForeignKey(to=Assignee, on_delete=models.CASCADE, blank=True, null=True)
    projects = models.ManyToManyField(Project, blank=True)

    objects = TaskManager()

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        # this fields will not be checked when __eq__ is called
        self.EQ_IGNORED_FIELDS.extend(['assignee_id', 'projects'])

    def save(self, from_django_admin=True, *args, **kwargs):
        # from_django_admin means the user hit the button Save in django-admin interface
        if from_django_admin:
            update_fields = ['name', 'notes']
            update_object = {key: value for key, value in self.__dict__.items() if key in update_fields}
            update_object['assignee'] = self.assignee_id
            if self.gid:
                self.api.client.tasks.update_task(self.gid, params=update_object)
            else:
                workspace_gid = list(self.api.client.workspaces.get_workspaces())[0]['gid']
                response = self.api.client.tasks.create_task(update_object, workspace=workspace_gid)
                self.gid = response['gid']

        print(f"[DB]Task {self.name} saving...")
        return super(Task, self).save(*args, **kwargs)
