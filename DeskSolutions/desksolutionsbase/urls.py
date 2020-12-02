from django.urls import path
from desksolutionsbase.views import OrganizationAction, signup, organizationlist

app_name = "signup"

urlpatterns = [
    path('', OrganizationAction, name="home"),
    path('organizations/', organizationlist, name="home"),
    path('profile/', signup, name='signups'),
]
