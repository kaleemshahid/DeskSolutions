from django.contrib import admin
from .models import Task, TaskDetail, TaskUpdate
from account.models import Profile

class TaskAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(qs)
        if request.user.is_admin:
            tasks = qs.filter(created_by__organization=request.user.organization)
            return tasks
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager:       
                related_user = qs.filter(created_by=request.user)
        except:
            pass
        return related_user
        

    def has_view_permission(self, request, obj=None):
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager:
                return True
        except:
            pass
        if request.user.is_admin:
            return True
        return False
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return True

class TaskDetailAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(qs)
        if request.user.is_admin:
            tasks = qs.filter(task__created_by_organization=request.user.organization)
            return tasks
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager: 
                related_user = qs.filter(task__created_by=request.user)
        except:
            pass
        return related_user
        
    def has_view_permission(self, request, obj=None):
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager:
                return True
        except:
            pass
        if request.user.is_admin:
            return True
        return False
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return True

class TaskUpdateAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(qs)
        if request.user.is_admin:
            tasks = qs.filter(taskdetail__task_created_by_organization=request.user.organization)
            return tasks
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager: 
                related_user = qs.filter(taskdetail__task_created_by=request.user)
        except:
            pass
        return related_user

    def has_view_permission(self, request, obj=None):
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager:
                return True
        except:
            pass
        if request.user.is_admin:
            return True
        return False
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return False

    def has_add_permission(self, request, obj=None):
        return True

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskDetail, TaskDetailAdmin)
admin.site.register(TaskUpdate, TaskUpdateAdmin)
# Register your models here.
