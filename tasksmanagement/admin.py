from django.contrib import admin
from .models import Task, TaskDetail, TaskUpdate
from account.models import Profile

class TaskAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager or request.user.is_admin:
                return True
        except:
            pass
        return False
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return False

    def has_add_permission(self, request, obj=None):
        return False

class TaskDetailAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager or request.user.is_admin:
                return True
        except:
            pass
        return False
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return False

    def has_add_permission(self, request, obj=None):
        return False

class TaskUpdateAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        try:
            get_profile = Profile.objects.get(pk=request.user.id)
            if get_profile.is_manager or request.user.is_admin:
                return True
        except:
            pass
        return False
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return False

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskDetail, TaskDetailAdmin)
admin.site.register(TaskUpdate, TaskUpdateAdmin)
# Register your models here.
