from django.urls import path
from desksolutionsbase.views import OrganizationAction, signup, organizationlist, jobs

app_name = "signup"

urlpatterns = [
    path('', organizationlist, name="home"),
    path('organizationsetup/', OrganizationAction, name="organization-register"),
    path('profile/', signup, name='signups'),
    path('jobs/<int:pk>/', jobs, name='jobs'),
    # path('applications/<int:pk>/', application, name='applications'),
]
