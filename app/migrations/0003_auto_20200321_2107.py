# Generated by Django 2.2.11 on 2020-03-21 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200321_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='notes',
            field=models.TextField(blank=True, default='text'),
            preserve_default=False,
        ),
    ]
