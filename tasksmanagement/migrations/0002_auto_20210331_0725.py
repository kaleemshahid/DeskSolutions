# Generated by Django 3.1.4 on 2021-03-31 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasksmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(max_length=20, verbose_name='Task Name'),
        ),
    ]
