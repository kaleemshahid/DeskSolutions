from django.urls import path
from desksolutionsbase.views import OrganizationAction, signup, organizationlist

app_name = "signup"

urlpatterns = [
    path('', organizationlist, name="home"),
    path('organizationsetup/', OrganizationAction, name="organization-register"),
    path('profile/', signup, name='signups'),
]
