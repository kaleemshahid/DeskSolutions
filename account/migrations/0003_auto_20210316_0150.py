# Generated by Django 3.1.4 on 2021-03-15 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210315_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='punch_in_time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]