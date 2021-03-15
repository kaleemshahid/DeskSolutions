from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator, FileExtensionValidator
# from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from .validators import validate_file_extension
from DeskSolutions import settings
from ckeditor.fields import RichTextField
# from django_google_maps import fields as map_fields
# from django.contrib.gis.db import models as gismodels

class Organization(models.Model):
    title = models.CharField(verbose_name="Organization Title",
                             max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(
        verbose_name="Description", null=True, blank=False)
    url = models.URLField(verbose_name="Organization URL",
                          null=True, blank=True, default=None)
    # org_location = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to="logos", default=None, null=True, blank=True)
    org_address = models.CharField(max_length=255,
        verbose_name="Organization Address", null=True, blank=False)
    city = models.CharField(max_length=40, null=False, blank=False, default=None)
    radius = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    # geoLocation = gismodels.PointField(max_length=100, null=True, blank=True, srid=4326)
    # geoLocation = models.CharField(max_length=100, null=True, blank=True)
    # objects = gismodels.Manager()

    def __str__(self):
        return self.title


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Email",
                              unique=True, null=False, blank=False)
    address = models.TextField(verbose_name="Address", null=True, blank=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=13, validators=[
                             phone_regex], blank=True)
    organization = models.ForeignKey(
        Organization, verbose_name="Organization", on_delete=models.CASCADE, null=True, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def get_group_permissions(self, obj):
        querset = User.objects.get(id=obj.id)
        return querset

# CompanyAdmins can then add their own departments, or add new users to their system but after adding departments
class Department(models.Model):
    department_name = models.CharField(
        max_length=60, null=False, blank=False, verbose_name="Department Name")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="Owned By", null=False, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name

class Tag(models.Model):
    keyword = models.CharField(max_length=15, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.keyword

class Position(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, default="Employee")
    responsibility = RichTextField(blank=False, null=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="Owned By", null=False, blank=True, default=None)
    tag = models.ManyToManyField(Tag, related_name="positiontag")
    job_posting = models.BooleanField(verbose_name="Open Position", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    candidate_email = models.CharField(max_length=20, null=False, blank=False, verbose_name="Email")
    candidate_name = models.CharField(max_length=20, null=False, blank=False, verbose_name="Name")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    candidate_phone = models.CharField(max_length=13, validators=[
                             phone_regex], blank=False, null=False)
    candidate_address = models.TextField(null=False, blank=False, default=None)
    filename = models.FileField(upload_to="applications", validators=[FileExtensionValidator(['pdf'])])
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_email

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, null=False)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=False, blank=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Attendance(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    punch_in_time = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=False)
    punch_out_time = models.DateTimeField(default=None, null=True)

class ComplaintBox(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, blank=False)
    complain_date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=250, null=False, blank=False)
    complain = models.CharField(max_length=250, null=False, blank=False)

    


