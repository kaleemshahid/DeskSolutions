from django import forms
from .models import Organization, Department, User, Profile
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string


# Model form for User Registration through admin panel
class UserModelForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super().__init__(*args, **kwargs)
    # password1 = forms.CharField(
    #     label="Password",
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'})
    # )

    # password2 = forms.CharField(
    #     label="Confirm Password",
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'})
    # )

    class Meta:
        model = User
        fields = ('email', 'organization', 'phone', 'address',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'phone': forms.TextInput(attrs={'class': 'form-control'}),
            # 'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     cpassword = get_random_string(length=7)
    #     user.set_password(cpassword)
    #     # user.set_password(self.cleaned_data['password1'])
    #     user.organization = self.request.user.organization
    #     user.is_admin = False
    #     if user:
    #         print("it happend")
    #         user.save()
    #     return user


class CustomDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("department_name", "user",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('department_name')

        get_deps = Department.objects.filter(
            department_name=name).filter(user__email=self.request.user)
        # get_organization = OrganizationHead.objects.filter(
        #     department_name=name).filter(organization__email=self.request.user)
        print(self.request.user)
        # get_deps = Department.objects.filter(name=name)
        # get_deps = Department.objects.filter(
        #     organization__email=self.user)

        # get_deps = CustomUser.objects.filter(department__name=name)
        if get_deps.count() != 0:
            raise forms.ValidationError(
                "This department already exists in the organization")


# class ProfileFormSet(BaseInlineFormSet):
#     '''
#     Validate formset data here
#     '''

#     def clean(self):
#         super().clean()

#         percent = 0
#         for form in self.forms:
#             print(form)
#             print(form.cleaned_data["department"])
#             # if form.cleaned_data["department"]
#             raise forms.ValidationError(
#                 _('Total of elements must be 100%%. Current : %(percent).2f%%') % {'percent': percent})

class ProfileFormSet(BaseInlineFormSet):

    def clean(self):
        try:
            for f in self.forms:
                department = f.cleaned_data.get('department')
                get_status = f.cleaned_data.get('is_manager')
                get_user = f.cleaned_data.get('organization_id')
                print(department.id)
                print(get_status)
                print(get_user)
                qs = Profile.objects.filter(
                    department=department.id, is_manager=True).count()

                if department is None:
                    raise ValidationError(
                        "One or more required fields is empty")
                if get_status:
                    if qs > 0:
                        raise ValidationError(
                            "A manager has already been allocated to selected Department")
        except AttributeError:
            pass
