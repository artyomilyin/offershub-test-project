# Generated by Django 2.2.11 on 2020-03-19 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('gid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
    ]
