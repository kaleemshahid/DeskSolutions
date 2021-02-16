# Generated by Django 3.1.4 on 2021-02-16 20:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_attendance_punch_in_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='punch_in_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
