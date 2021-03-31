from django.contrib import admin
from .models import Task, TaskDetail, TaskUpdate
from account.models import Profile

class TaskUpdateInline(admin.TabularInline):
    model = TaskUpdate
    min_num =1

class TaskDetailInline(admin.TabularInline):
    model = TaskDetail
    min_num = 1


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name','created_by','is_completed', 'created_at')
    list_filter = ('is_completed', )
    ordering = ('created_at',)
    fieldsets = (
            ("Information", {'fields': ('task_name', 'is_completed', 'created_at', 'created_by')}),
        )
    inlines = [
        TaskDetailInline,
    ]

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
        return False

class TaskDetailAdmin(admin.ModelAdmin):

    list_display = ('task','assigned_to', 'priority', 'start_time')
    list_filter = ('priority', )
    ordering = ('start_time',)
    fieldsets = (
            ("Information", {'fields': ('task','assigned_to', 'description', 'priority', 'start_time')}),
        )
    inlines = [
        TaskUpdateInline,
    ]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        a = qs.filter(task__created_by__organization=request.user.organization)
        print(a)
        if request.user.is_admin:
            tasks = qs.filter(task__created_by__organization=request.user.organization)
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
        return False

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
                related_user = qs.filter(taskdetail__task__created_by=request.user)
                return related_user
        except:
            pass

    def has_view_permission(self, request, obj=None):
        # try:
        #     get_profile = Profile.objects.get(pk=request.user.id)
        #     if get_profile.is_manager:
        #         return True
        # except:
        #     pass
        # if request.user.is_admin:
        #     return True
        return False
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # if request.user.is_admin:
        return False

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskDetail, TaskDetailAdmin)
admin.site.register(TaskUpdate, TaskUpdateAdmin)
# Register your models here.
