# Generated by Django 2.2.11 on 2020-03-19 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200319_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('gid', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('notes', models.TextField()),
                ('assignee', models.CharField(max_length=250)),
            ],
        ),
    ]