# Generated by Django 3.1.4 on 2021-02-16 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210216_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='punch_in_time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]