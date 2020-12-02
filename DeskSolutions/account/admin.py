from django.contrib import admin
from .models import Organization, User, Department, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserModelForm, CustomDepartmentForm, ProfileFormSet
from django.contrib.auth.models import Group, Permission
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages


class ProfileInline(admin.TabularInline):
    model = Profile
    formset = ProfileFormSet
    min_num = 1
    # fieldsets = (
    #     (None, {'fields': ('is_manager', 'department')}),
    # )
    # add_fieldsets = (
    #     ('Personal Information', {
    #         'fields': ('organization_email', 'organization_name', 'department', 'is_staff', 'is_active', 'groups',)}
    #      ),
    # )

    def get_formset(self, request, obj=None, **kwargs):
        # if obj:
        if obj.is_admin:
            kwargs['exclude'] = ('is_manager',)
        return super().get_formset(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return False


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('is_manager',)
#     fieldsets = (
#         (None, {'fields': ('is_manager', 'department',)}),
#     )


class UserAdmin(BaseUserAdmin):
    add_form = UserModelForm
    model = User
    inlines = [
        ProfileInline,
    ]

    # empty_value_display = "NA"

    def changelist_view(self, request, extra_context=None):
        qs = Organization.objects.get(user__id=request.user.id)
        depts = Department.objects.filter(user_id=request.user.id)
        for dep in depts:
            check_manager = Profile.objects.filter(
                department=dep.id, is_manager=True).count()
            # for status in check_manager:
            # if not status.is_manager:
            if check_manager < 1:
                messages.warning(request, dep.department_name +
                                 " needs action. No Manager specified for the department")
        extra_context = {'title': qs.title}

        return super(UserAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide inline in the add view
            # we are on change page if the below condition is TRUE
            if obj is None or not obj.is_admin:
                yield inline.get_formset(request, obj), inline

    list_display = ('email',
                    'is_admin', 'manager')
    list_filter = ('is_superuser', 'is_staff', )
    ordering = ('email',)
    filter_horizontal = ()

    def manager(self, obj):
        # return "\n".join([str(p.is_manager) for p in Profile.objects.filter(organization=obj.id)])
        q = Profile.objects.get(organization__id=obj.id)
        return q.is_manager
    # This would set the method type to Boolean
    manager.boolean = True
    manager.empty_value_display = "NA"

    # fieldsets = (
    #     ("Information", {'fields': ('email', 'phone', 'address')}),
    #     ('Permissions', {'fields': ('is_staff',
    #                                 'is_active',)}),
    # )

    # def get_user(self, obj):
    #     return obj.get_user()

    # def get_fieldsets(self, request, obj=None):
    #     fs = [
    #         ("see",  {'fields': ['address', ]}),
    #         ('Map', {'fields': [],  # required by django admin
    #                  'description':obj.get_user(),
    #                  }),
    #     ]
    #     print(obj.get_user())
    #     return fs

    # def get_fieldsets(self, request, obj=None):
    #     fields = super().get_fields(request, obj)
    #     if obj:
    #         fields_to_remove = []
    #         if request.user.is_superuser:
    #             fields_to_remove = ['is_admin', ]
    #             for field in fields_to_remove:
    #                 fields.remove(field)
    #         return fields

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return []
    #     return self.readonly_fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(
            UserAdmin, self).get_readonly_fields(request, obj)
        if obj and obj.is_admin:  # editing an existing object
            print("obj.is_admin is None")
            return readonly_fields + ('is_active', 'is_staff',)
        print("obj.is_admin is not None")
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        if request.user.is_admin:
            # print("yesss")
            # print(request.user.password)
            # fs = ((None, {'fields': ('email', 'title', 'phone', 'description', 'url', 'password', 'is_staff',
            #                          'is_active', 'is_manager', 'groups',)}))
            fs = (
                ("Information", {'fields': ('email', 'phone', 'address')}),
                ('Permissions', {'fields': ('is_staff',
                                            'is_active',)}),
            )

            # exclude = ('password2',)
            return fs
        else:
            # fs = ((None, {'fields': ('email', 'title', 'phone',
            #                          'description', 'password')}))
            fs = (
                ("Information", {'fields': ('email', 'phone', 'address')}),
                ('Permissions', {'fields': ('is_staff',
                                            'is_active',)}),
            )
            return fs

    # return fs

    # def get_fieldsets(self, request, obj=None):
    #     fs = super().get_fieldsets(request, obj)
    #     # fs now contains [(None, {'fields': fields})], do with it whatever you want
    #     fs[0][1]['fields': ('email'), ]
    #     return fs
    # else:
    # return ("Information", {'fields': ('email', 'title', 'phone',
    #    'description', 'password')})

    # /////// yhqn aik function bna k dekho, jo groups field ko replace kr k custom group dy

    # add_fieldsets = (
    #     ('Personal Information', {
    #         # To create a section with name 'Personal Information' with mentioned fields
    #         'description': "added_by",
    #         # To make char fields and text fields of a specific size
    #         'classes': ('wide',),
    #         'fields': ('email', 'phone', 'address', 'is_staff',
    #                    'is_active', 'groups',)}
    #      ),
    # )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_admin:
            return qs.filter(organization_id=request.user.organization)
        return qs.filter(id=request.user.id)

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

# 9/11/2020, rat 9.16 pe isko comment kia tha meny, ku k mjy lgta tha k iski koi zrurt ni
    def save_model(self, request, obj, form, change):
        user = request.user
        obj = form.save(commit=False)
        password = get_random_string(length=7)
        print(user)
        print(obj)
        print(password)
        if obj and not change:
            obj.organization = user.organization
            obj.set_password(password)
            obj.is_admin = False

        obj.save()
        # send_mail('This is your passwrd', password,'noreply@desksolutions.com', [obj], fail_silently = False)
        return obj

    # def get_form(self, request, obj=None, **kwargs):
    #     UserForm = super().get_form(request, obj, **kwargs)

    #     class UserFormWithRequest(UserForm):
    #         def __new__(cls, *args, **kwargs):
    #             kwargs['request'] = request
    #             return UserForm(*args, **kwargs)
    #     return UserFormWithRequest


class DepartmentAdmin(admin.ModelAdmin):

    form = CustomDepartmentForm
    list_display = ('department_name', 'user')
    list_filter = ('department_name',)
    ordering = ('department_name',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('department_name',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin or request.user.is_superuser:
            return True
        return False

    def save_model(self, request, obj, form, change):
        # if obj.organization:
        #     obj.organization = request.user
        #     obj.save()

        user = request.user
        # if user
        obj = form.save(commit=False)
        if not change or not obj.user:
            obj.user = user
        # instance.modified_by = user
        obj.save()
        # form.save_m2m()
        return obj

    def get_form(self, request, obj=None, **kwargs):
        DepartmentForm = super().get_form(request, obj, **kwargs)

        class DepartmentFormWithRequest(DepartmentForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return DepartmentForm(*args, **kwargs)
        return DepartmentFormWithRequest


class OrganizationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_admin:
            return qs.filter(user__id=request.user.id)
        return qs

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin or request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Department, DepartmentAdmin)
# admin.site.register(Profile)
