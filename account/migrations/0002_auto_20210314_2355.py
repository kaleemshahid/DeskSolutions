# Generated by Django 3.1.4 on 2021-03-14 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='punch_in_time',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='punch_out_time',
            field=models.TimeField(default=None, null=True),
        ),
    ]