from django.contrib import admin
from .models import Task, TaskDetail, TaskUpdate

admin.site.register(Task)
admin.site.register(TaskDetail)
admin.site.register(TaskUpdate)
# Register your models here.
