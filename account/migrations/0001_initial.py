# Generated by Django 3.1.4 on 2021-03-14 21:11

import ckeditor.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Organization Title')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('url', models.URLField(blank=True, default=None, null=True, verbose_name='Organization URL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ImageField(blank=True, default=None, null=True, upload_to='logos')),
                ('org_address', models.CharField(max_length=255, null=True, verbose_name='Organization Address')),
                ('city', models.CharField(default=None, max_length=40)),
                ('radius', models.IntegerField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Employee', max_length=20)),
                ('responsibility', ckeditor.fields.RichTextField()),
                ('job_posting', models.BooleanField(default=False, verbose_name='Open Position')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='account.organization', verbose_name='Owned By')),
                ('tag', models.ManyToManyField(related_name='positiontag', to='account.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=60, verbose_name='Department Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='account.organization', verbose_name='Owned By')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_email', models.CharField(max_length=20, verbose_name='Email')),
                ('candidate_name', models.CharField(max_length=20, verbose_name='Name')),
                ('candidate_phone', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('candidate_address', models.TextField(default=None)),
                ('filename', models.FileField(upload_to='applications', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.position')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('address', models.TextField(null=True, verbose_name='Address')),
                ('phone', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.organization', verbose_name='Organization')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.user')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_manager', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.department')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.position')),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain_date', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=250)),
                ('complain', models.TextField()),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('punch_in_time', models.DateTimeField(auto_now_add=True)),
                ('is_present', models.BooleanField(default=False)),
                ('punch_out_time', models.DateTimeField(default=None, null=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
    ]
