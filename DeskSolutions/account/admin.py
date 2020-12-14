from django.contrib import admin
from .models import Organization, User, Department, Profile, Position, Tag, Application
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserModelForm, CustomDepartmentForm, ProfileFormSet, PositionForm
from django.contrib.auth.models import Group, Permission
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
import pdfplumber, operator, collections

# from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from django.template.response import TemplateResponse
from django.urls import path

class ApplicationAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('appreview/', self.admin_site.admin_view(self.app_review), name="appreview"),
        ]
        return my_urls + urls

    change_list_template = 'admin/application.html'

    def app_review(self, request):
        context = {}
        arraylist = []
        textList = []
        appsList = []
        app_dict = {}
        getapps = Application.objects.filter(position__organization_id=request.user.organization)
        print(getapps)
        position = Position.objects.filter(organization=request.user.organization, job_posting=True, application__in=getapps)
        print(position)
        
        # tags = Tag.objects.filter()
        for pos in position:
            # print(pos)
            position_tags = list(pos.tag.all().values_list('keyword', flat=True))
            print(position_tags)
            # [['flask', 'django'], ['expert', 'resume']]
            # made the position_tags a list cz wwe want the results in individual lists
            # print(position_tags)
            arraylist.append(position_tags)
            # for p in position_tags:
            #     print(p)
            #     # arraylist.append(p.keyword)
            #     appsList.append(p)
                # print(p)
            # arraylist.append(p)
            print(arraylist)
        # print(arraylist)
        # print(appsList)
        # for t in tags:
        #     # print(t.keyword)
        #     arraylist.append(t.keyword)
        # print(arraylist)
        # count = 0
        for count, i in enumerate(getapps):
            print("count: " + str(count))
            # print(i.pk)
            pdf = pdfplumber.open('media/' + str(i.filename))
            print(i.candidate_email)
            print(i.filename)
            page = pdf.pages[0]
            text = page.extract_text().split()

            print(text)
            # for count2, s in enumerate(arraylist):
            # print(text)
            # print(count2)
            # print(arraylist)
            a = set(arraylist[count]).intersection(text)
            # print(count)
            print(a)
            # print(sorted(list(a), reverse=True))
            b = list(a)
            # print(b)
            # print(b)
            # b.sort(reverse=False)
            # print(b)
            # print(len(a))
            # print(len(list(a)))
            app_dict[i.pk] = len(b)

            # c =textList.append(b)
            print(app_dict[i.pk])
            
            d = len(textList)

            # count = count + 1
            # print(pdf)
            # print(textList.index)

            # print(len(sorted(textList, reverse=True)))
            # print(sorted(textList, reverse=True))
            # print(textList.append(list(a)))

            # print(len(b))
        # print(sorted(textList, reverse=True))
        
        # sorted_d = sorted(app_dict.items(), key=operator.itemgetter(1), reverse=True)
        # print(app_dict)
        sorted_d = collections.OrderedDict(sorted(app_dict.items(), key=lambda x: x[1], reverse=True))
        sorted_dict = dict(sorted_d)
        print(sorted_dict)
        # for m in sorted_dict:
        #     print(m, sorted_dict[m])
        # sorted_list = list(sorted_d.keys())
        # print(sorted_list)
        # sorted_values = list(sorted_d.values())
        # print(sorted_values)
        for s in sorted_dict:
            print(s, sorted_dict[s])
            appsList.append(sorted_dict[s])
            for app in appsList:
                print(app)
                context["mat_length"] = sorted_dict
            print(context["mat_length"])
            
            filtered_applications = getapps.filter(pk=s)
            for f in filtered_applications:
            # print(filtered_applications)
                textList.append(f)
            # textList.append(filtered_applications)
        # print(textList)
        # for v in sorted_values:
        #     print(v)
        #     appsList.append(v)
        
        context['getapps'] = textList
        
        # context['getappss'] = getapps
        # print(textList)
        # print(textList.sort())
        #     # b = list(a)
        # print(textList)
        
        # tagsList = list(tags)
        # print(tagsList)

        context['basecontext'] = self.admin_site.each_context(request)

        # for pdf in getapps:
        #     # print('media/' + str(pdf.filename))
        #     pdf = pdfplumber.open('media/' + str(pdf.filename))
        #     page = pdf.pages[0]
        #     text = page.extract_text().split()
        #     print(text)

        # pdf = pdfplumber.open('media/applications/dummy.pdf')
        # page = pdf.pages[0]
        # text = page.extract_text()
        # s = text.split()
        # context["text"] = text.split()
        # for t in s:
        #     print(t)
        #     context["t"] = t
        #     if t == "file":
        #         print("found this")
        # context = dict(
        #    # Include common variables for rendering the admin template.
        #    self.admin_site.each_context(request),
           
        #    # Anything else you want in the context...
        #     # key=value,
        #     'getapps'= getapps,
        # )
        return TemplateResponse(request, "account/applicationportal.html", context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_admin:
            return qs.filter(position__organization_id=request.user.organization)
        return qs

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return False

    def has_module_permission(self, request):
        if request.user.is_admin:
            return True
        return False

    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict thus hiding the model from admin index.
    #     """
    #     return {}

class ProfileInline(admin.TabularInline):
    model = Profile
    formset = ProfileFormSet
    min_num = 1

    # Override for displaying only relative department of an organization instead of all
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(ProfileInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        print(field)
        if db_field.name == 'department':
            if request.user is not None:
                print(field.queryset)
                field.queryset = field.queryset.filter(organization__exact = request.user.organization)  
            else:
                field.queryset = field.queryset.none()

        return field
    # fieldsets = (
    #     (None, {'fields': ('is_manager', 'department')}),
    # )
    # add_fieldsets = (
    #     ('Personal Information', {
    #         'fields': ('organization_email', 'organization_name', 'department', 'is_staff', 'is_active', 'groups',)}
    #      ),
    # )

    # PAY ATTENTION TO THIS FORMSET, I REMOVED IT COSIDERING THE ADDED FUNCTIONALITY OF WARNING MESSAGES
    # def get_formset(self, request, obj=None, **kwargs):
    #     # if obj:
    #     if obj.is_admin:
    #         kwargs['exclude'] = ('is_manager',)
    #     return super().get_formset(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
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

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('organization','department','is_manager')
    list_filter = ('department', )
    ordering = ('organization',)
    filter_horizontal = ()

    readonly_fields = ('organization','department', 'position', 'is_manager')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        related_user = qs.filter(organization=request.user)
        for i in related_user:
            pass
        return qs.filter(department=i.department)

    def changelist_view(self, request, extra_context=None):
        try:
            qs = Profile.objects.get(organization__id=request.user.id)
            extra_context = {'title': qs.department}
        except Profile.DoesNotExist:
            pass

        return super(ProfileAdmin, self).changelist_view(request, extra_context=extra_context)
    def has_view_permission(self, request, obj=None):
        if request.user.is_admin or request.user.is_superuser:
            return False
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class UserAdmin(BaseUserAdmin):
    add_form = UserModelForm
    model = User
    inlines = [
        ProfileInline,
    ]

    # empty_value_display = "NA"

    def changelist_view(self, request, extra_context=None):
        if request.user.is_admin:
            try:
                qs = Organization.objects.get(user__id=request.user.id)
                extra_context = {'title':qs.title}
            except Organization.DoesNotExist:
                pass
            depts = Department.objects.filter(organization=request.user.organization)
            for dep in depts:
                check_manager = Profile.objects.filter(
                    department=dep.id, is_manager=True).count()
                # for status in check_manager:
                # if not status.is_manager:
                if check_manager < 1:
                    messages.warning(request, dep.department_name +
                                    " needs action. No Manager specified for the department")

        return super(UserAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide inline in the add view
            # we are on change page if the below condition is TRUE
            if obj is None or not obj.is_admin:
                yield inline.get_formset(request, obj), inline

    list_display = ('email',
                    'is_admin', 'manager')
    list_filter = ('is_superuser', 'is_staff',)
    ordering = ('email',)
    search_fields = ('email',)

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
        try:
            get_profile = Profile.objects.get(organization=request.user)
            if get_profile.is_manager:
                print(request.user.is_admin)
                return True
        except:
            pass
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
    list_display = ('department_name', 'organization')
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
        return qs.filter(organization=request.user.organization)

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin or request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        # return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    # def has_module_permission(self, request):
    #     if request.user.is_admin:
    #         return True
    #     return False

    

    # def has_module_permission(self, request):
    #     if request.user.is_admin:
    #         return True
    #     return False

    def save_model(self, request, obj, form, change):
        # if obj.organization:
        #     obj.organization = request.user
        #     obj.save()

        user = request.user
        # if user
        obj = form.save(commit=False)
        if not change or not obj.organization:
            obj.organization = user.organization
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
        if request.user.is_superuser:
            return True
        return False

    # def has_module_permission(self, request):
    #     if request.user.is_admin:
    #         return True
    #     return False

class PositionAdmin(admin.ModelAdmin):

    form = PositionForm
    list_display = ('title', 'organization')
    list_filter = ('title',)
    ordering = ('title',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('title','responsibility', 'tag', 'job_posting')}),
    )
    exclude = ('owned_by',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.organization)

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

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def save_model(self, request, obj, form, change):
        user = request.user
        obj = form.save(commit=False)
        if not change or not obj:
            print("postion not change true")
            obj.organization = user.organization
        print(change)
        print(obj)
        obj.save()
        return obj
        
    def get_form(self, request, obj=None, **kwargs):
        PosForm = super().get_form(request, obj, **kwargs)

        class PositionFormWithRequest(PosForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return PosForm(*args, **kwargs)
        return PositionFormWithRequest

admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Tag)
admin.site.register(Application, ApplicationAdmin)
# admin.site.register(MyModelAdmin)

admin.site.unregister(Group)

