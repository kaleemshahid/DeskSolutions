# django imports
from django.urls import include, path
# rest-framework imports
from rest_framework.routers import DefaultRouter
from .views import UserLoginApiView, LogoutApiView, EmployeeViewSet, OrganizationViewSet

urlpatterns = [
    path('employee/', EmployeeViewSet.as_view()),
    path('login/', UserLoginApiView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name="logout"),
    path('organizationupdate/', OrganizationViewSet.as_view(), name="orgupdate"),
]
