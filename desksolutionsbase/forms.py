from django import forms
from account.models import Organization, User, Profile, Application

class LookupForm(forms.Form):
    organization_name = forms.CharField(
        max_length=40, 
        required=True,
        widget=forms.TextInput(
            attrs={
            'class': 'form-control input-text',
            'placeholder' : 'Enter exact organization name',
            }
            )
        )

class ContactForm(forms.Form):
    contact_email = forms.EmailField(
        max_length=60,
        required=True,
        widget= forms.EmailInput(
            attrs={
                'class' : 'form-control input-text',
                'placeholder' : "Your email address...",
            }
            )
        )

    contact_name = forms.CharField(
        max_length=60,
        required=True,
        widget= forms.TextInput(
            attrs={
                'class' : 'form-control input-text',
                'placeholder' : "Your name...",
            }
            )
        )
    
    contact_message = forms.CharField(
            required=True,
            widget= forms.Textarea(
            attrs={
                'class' : 'form-control input-text',
                'placeholder' : "Your message...",
            }
            )
        
        )

    

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('title', 'url', 'description', 'org_address','city', 'logo')
        widgets = {
            'title': forms.EmailInput(attrs={
                'class': 'form-control input-text',
                # 'placeholder' : 'Organization Email',
                }),
            'url': forms.TextInput(attrs={
                'class': 'form-control input-text',
                # 'placeholder' : 'Organization URL',
                }),
            'description': forms.Textarea(attrs={
                'class': 'form-control input-text',
                'rows': 3,
                'placeholder' : 'Describe your organization in few words...',
                }),
            'org_address': forms.Textarea(attrs={
                'class': 'form-control input-text', 
                'rows': 1,
                'placeholder' : 'House no 1, Street 44, Model Town, Lahore',
                }),
            # 'logo': forms.FileField(allow_empty_file=True),
        }
        


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control input-text'})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control input-text'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control input-text'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control input-text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control input-text'}),
            'phone': forms.TextInput(attrs={'class': 'form-control input-text'}),
            'address': forms.Textarea(attrs={'class': 'form-control input-text'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control input-text'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            # print("it happend")
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('is_manager',)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('candidate_email', 'candidate_name', 'candidate_phone', 'candidate_address', 'filename')
        widgets = {
            'candidate_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'candidate_name': forms.TextInput(attrs={'class': 'form-control'}),
            'candidate_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'candidate_address': forms.Textarea(attrs={'class': 'form-control'}),
            'filename': forms.FileInput(attrs={'class': 'form-control'}),
        }