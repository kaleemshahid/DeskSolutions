# django imports
from django.urls import include, path
# rest-framework imports
from rest_framework.routers import DefaultRouter
from .views import UserLoginApiView, LogoutApiView, EmployeeViewSet, AttendanceViewSet, ComplaintBoxViewSet, OrganizationViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('employee/', EmployeeViewSet.as_view()),
    path('login/', UserLoginApiView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name="logout"),
    path('organization/', OrganizationViewSet.as_view(), name="orgupdate"),
    path('', include(router.urls)),
    # path('attendance/', AttendanceViewSet.as_view(), name="attendance"),
    path('complaint/', ComplaintBoxViewSet.as_view(), name="attendance"),
]
