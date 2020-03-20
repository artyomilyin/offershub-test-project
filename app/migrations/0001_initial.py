# Generated by Django 2.2.11 on 2020-03-20 18:53

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignee',
            fields=[
                ('gid', models.CharField(editable=False, max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
            bases=(models.Model, app.models.WithAPI),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('gid', models.CharField(editable=False, max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
            bases=(models.Model, app.models.WithAPI),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('gid', models.CharField(editable=False, max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('notes', models.TextField()),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Assignee')),
                ('projects', models.ManyToManyField(to='app.Project')),
            ],
            bases=(models.Model, app.models.WithAPI),
        ),
    ]
