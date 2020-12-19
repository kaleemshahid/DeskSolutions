# Generated by Django 3.1.4 on 2020-12-05 14:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20201205_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='filename',
            field=models.FileField(upload_to='applications', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]