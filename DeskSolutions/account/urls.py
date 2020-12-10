# django imports
from django.urls import include, path
# rest-framework imports
from rest_framework.routers import DefaultRouter
from .views import UserLoginApiView, LogoutApiView

urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name="logout" )
]
